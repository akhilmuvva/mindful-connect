"""
Mood Prediction using Machine Learning
Predicts future mood trends using Scikit-learn
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import List, Dict, Any, Optional, Tuple
import joblib
from datetime import datetime, timedelta
import logging

from src.config import settings, MODELS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MoodPredictor:
    """ML-based mood forecasting"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.lookback_days = settings.MOOD_PREDICTION_LOOKBACK_DAYS
        self.forecast_days = settings.MOOD_PREDICTION_FORECAST_DAYS
        self.model_path = MODELS_DIR / "mood_predictor.joblib"
        self.scaler_path = MODELS_DIR / "mood_scaler.joblib"
        
        # Try to load existing model
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model if exists"""
        try:
            if self.model_path.exists():
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                logger.info("Loaded existing mood prediction model")
            else:
                logger.info("No existing model found, will train on first use")
        except Exception as e:
            logger.warning(f"Could not load model: {e}")
    
    def _save_model(self):
        """Save trained model"""
        try:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            logger.info("Mood prediction model saved")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
    
    def prepare_features(self, mood_history: List[Dict[str, Any]]) -> Optional[pd.DataFrame]:
        """
        Prepare features from mood history
        
        Args:
            mood_history: List of mood entries
            
        Returns:
            DataFrame with features or None
        """
        try:
            if len(mood_history) < 7:  # Need at least a week of data
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(mood_history)
            
            # Ensure datetime
            if 'created_at' in df.columns:
                df['date'] = pd.to_datetime(df['created_at'])
            else:
                return None
            
            # Sort by date
            df = df.sort_values('date')
            
            # Extract features
            df['day_of_week'] = df['date'].dt.dayofweek
            df['day_of_month'] = df['date'].dt.day
            df['month'] = df['date'].dt.month
            df['hour'] = df['date'].dt.hour
            
            # Mood score (target variable)
            if 'mood_score' not in df.columns:
                return None
            
            # Rolling statistics
            df['mood_rolling_mean_3'] = df['mood_score'].rolling(window=3, min_periods=1).mean()
            df['mood_rolling_std_3'] = df['mood_score'].rolling(window=3, min_periods=1).std().fillna(0)
            df['mood_rolling_mean_7'] = df['mood_score'].rolling(window=7, min_periods=1).mean()
            
            # Lag features
            df['mood_lag_1'] = df['mood_score'].shift(1).fillna(df['mood_score'].mean())
            df['mood_lag_2'] = df['mood_score'].shift(2).fillna(df['mood_score'].mean())
            df['mood_lag_7'] = df['mood_score'].shift(7).fillna(df['mood_score'].mean())
            
            # Trend
            df['mood_trend'] = df['mood_score'].diff().fillna(0)
            
            return df
            
        except Exception as e:
            logger.error(f"Feature preparation failed: {e}")
            return None
    
    def train_model(self, mood_history: List[Dict[str, Any]]) -> bool:
        """
        Train mood prediction model
        
        Args:
            mood_history: Historical mood data
            
        Returns:
            Success status
        """
        try:
            df = self.prepare_features(mood_history)
            
            if df is None or len(df) < 14:
                logger.warning("Insufficient data for training")
                return False
            
            # Select features
            feature_cols = [
                'day_of_week', 'day_of_month', 'month', 'hour',
                'mood_rolling_mean_3', 'mood_rolling_std_3', 'mood_rolling_mean_7',
                'mood_lag_1', 'mood_lag_2', 'mood_lag_7', 'mood_trend'
            ]
            
            X = df[feature_cols].values
            y = df['mood_score'].values
            
            # Remove NaN values
            mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
            X = X[mask]
            y = y[mask]
            
            if len(X) < 10:
                logger.warning("Not enough clean data for training")
                return False
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model (using Gradient Boosting for better performance)
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=3,
                random_state=42
            )
            
            self.model.fit(X_scaled, y)
            
            # Save model
            self._save_model()
            
            logger.info(f"Model trained successfully with {len(X)} samples")
            return True
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return False
    
    def predict_mood(self, mood_history: List[Dict[str, Any]], 
                    days_ahead: int = 7) -> Optional[Dict[str, Any]]:
        """
        Predict future mood trends
        
        Args:
            mood_history: Historical mood data
            days_ahead: Number of days to forecast
            
        Returns:
            Predictions or None
        """
        try:
            # Train or retrain model if needed
            if self.model is None:
                if not self.train_model(mood_history):
                    return None
            
            df = self.prepare_features(mood_history)
            
            if df is None:
                return None
            
            # Get latest features
            feature_cols = [
                'day_of_week', 'day_of_month', 'month', 'hour',
                'mood_rolling_mean_3', 'mood_rolling_std_3', 'mood_rolling_mean_7',
                'mood_lag_1', 'mood_lag_2', 'mood_lag_7', 'mood_trend'
            ]
            
            # Make predictions for next N days
            predictions = []
            last_date = df['date'].iloc[-1]
            last_features = df[feature_cols].iloc[-1].values
            
            for i in range(days_ahead):
                # Predict next day
                X_pred = last_features.reshape(1, -1)
                X_pred_scaled = self.scaler.transform(X_pred)
                
                predicted_mood = self.model.predict(X_pred_scaled)[0]
                
                # Clip to valid range
                predicted_mood = np.clip(predicted_mood, 1, 10)
                
                # Calculate prediction date
                pred_date = last_date + timedelta(days=i+1)
                
                predictions.append({
                    "date": pred_date.strftime("%Y-%m-%d"),
                    "predicted_mood": round(float(predicted_mood), 2),
                    "mood_label": self._get_mood_label(int(predicted_mood))
                })
                
                # Update features for next iteration (simplified)
                # In a real scenario, you'd update all rolling features
                last_features[7] = predicted_mood  # mood_lag_1
            
            logger.info(f"Generated {len(predictions)} day mood forecast")
            
            return {
                "success": True,
                "predictions": predictions,
                "forecast_days": days_ahead,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Mood prediction failed: {e}")
            return None
    
    def _get_mood_label(self, score: int) -> str:
        """Convert mood score to label"""
        if score >= 9:
            return 'excellent'
        elif score >= 7:
            return 'good'
        elif score >= 5:
            return 'okay'
        elif score >= 3:
            return 'low'
        else:
            return 'very_low'
    
    def get_mood_insights(self, mood_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistical insights from mood history
        
        Args:
            mood_history: Historical mood data
            
        Returns:
            Statistical insights
        """
        try:
            if not mood_history:
                return {"success": False, "error": "No mood history"}
            
            df = pd.DataFrame(mood_history)
            
            if 'mood_score' not in df.columns:
                return {"success": False, "error": "No mood scores found"}
            
            mood_scores = df['mood_score'].values
            
            insights = {
                "success": True,
                "average_mood": round(float(np.mean(mood_scores)), 2),
                "mood_std": round(float(np.std(mood_scores)), 2),
                "min_mood": int(np.min(mood_scores)),
                "max_mood": int(np.max(mood_scores)),
                "median_mood": round(float(np.median(mood_scores)), 2),
                "mood_volatility": "high" if np.std(mood_scores) > 2 else "moderate" if np.std(mood_scores) > 1 else "low",
                "total_entries": len(mood_scores)
            }
            
            # Trend analysis
            if len(mood_scores) >= 7:
                recent_avg = np.mean(mood_scores[-7:])
                older_avg = np.mean(mood_scores[:-7]) if len(mood_scores) > 7 else recent_avg
                
                if recent_avg > older_avg + 0.5:
                    insights["trend"] = "improving"
                elif recent_avg < older_avg - 0.5:
                    insights["trend"] = "declining"
                else:
                    insights["trend"] = "stable"
            else:
                insights["trend"] = "insufficient_data"
            
            logger.info("Generated mood insights")
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate insights: {e}")
            return {"success": False, "error": str(e)}


# Singleton instance
mood_predictor = MoodPredictor()
