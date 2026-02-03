"""
Sentiment Analysis using Hugging Face Transformers
Analyzes mood from journal text using NLP
"""

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Any, Optional
import logging

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SentimentAnalyzer:
    """NLP-based sentiment analysis for mood tracking"""
    
    def __init__(self):
        self.model_name = settings.SENTIMENT_MODEL
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the sentiment analysis model"""
        try:
            logger.info(f"Loading sentiment model: {self.model_name}")
            
            # Load model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            
            # Create pipeline
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("Sentiment model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            raise
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        try:
            if not text or len(text.strip()) == 0:
                return {
                    "success": False,
                    "error": "Empty text provided"
                }
            
            # Truncate if too long
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]
            
            # Run sentiment analysis
            result = self.sentiment_pipeline(text)[0]
            
            # Map to mood scale (1-10)
            label = result['label'].upper()
            confidence = result['score']
            
            if label == 'POSITIVE':
                mood_score = int(5 + (confidence * 5))  # 5-10
                mood_label = self._get_mood_label(mood_score)
            elif label == 'NEGATIVE':
                mood_score = int(5 - (confidence * 4))  # 1-5
                mood_label = self._get_mood_label(mood_score)
            else:
                mood_score = 5
                mood_label = 'neutral'
            
            logger.info(f"Sentiment analyzed: {mood_label} (score: {mood_score})")
            
            return {
                "success": True,
                "sentiment": label.lower(),
                "confidence": round(confidence, 3),
                "mood_score": mood_score,
                "mood_label": mood_label,
                "raw_result": result
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_mood_label(self, score: int) -> str:
        """
        Convert mood score to label
        
        Args:
            score: Mood score (1-10)
            
        Returns:
            Mood label
        """
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
    
    def analyze_mood_entry(self, mood_entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze complete mood entry
        
        Args:
            mood_entry: Mood entry with journal text
            
        Returns:
            Enhanced mood entry with sentiment analysis
        """
        try:
            journal_text = mood_entry.get('journal_text', '')
            
            if journal_text:
                sentiment_result = self.analyze_text(journal_text)
                
                if sentiment_result['success']:
                    mood_entry['ai_sentiment'] = sentiment_result['sentiment']
                    mood_entry['ai_confidence'] = sentiment_result['confidence']
                    mood_entry['ai_mood_score'] = sentiment_result['mood_score']
                    mood_entry['ai_mood_label'] = sentiment_result['mood_label']
            
            return mood_entry
            
        except Exception as e:
            logger.error(f"Failed to analyze mood entry: {e}")
            return mood_entry
    
    def extract_emotions(self, text: str) -> Dict[str, Any]:
        """
        Extract specific emotions from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected emotions
        """
        try:
            # Use zero-shot classification for emotion detection
            emotion_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=0 if torch.cuda.is_available() else -1
            )
            
            emotions = [
                "joy", "sadness", "anger", "fear", 
                "anxiety", "calm", "excited", "stressed"
            ]
            
            result = emotion_classifier(text, emotions, multi_label=True)
            
            # Get top 3 emotions
            top_emotions = []
            for label, score in zip(result['labels'][:3], result['scores'][:3]):
                if score > 0.3:  # Threshold
                    top_emotions.append({
                        "emotion": label,
                        "confidence": round(score, 3)
                    })
            
            logger.info(f"Extracted emotions: {[e['emotion'] for e in top_emotions]}")
            
            return {
                "success": True,
                "emotions": top_emotions,
                "all_scores": dict(zip(result['labels'], result['scores']))
            }
            
        except Exception as e:
            logger.error(f"Emotion extraction failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def detect_triggers(self, text: str) -> Dict[str, Any]:
        """
        Detect potential mood triggers from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Detected triggers
        """
        try:
            # Common trigger categories
            trigger_categories = [
                "work stress", "relationship issues", "health concerns",
                "financial worries", "social anxiety", "sleep problems",
                "family conflict", "loneliness"
            ]
            
            # Use zero-shot classification
            classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=0 if torch.cuda.is_available() else -1
            )
            
            result = classifier(text, trigger_categories, multi_label=True)
            
            # Get triggers above threshold
            detected_triggers = []
            for label, score in zip(result['labels'], result['scores']):
                if score > 0.4:  # Threshold
                    detected_triggers.append({
                        "trigger": label,
                        "confidence": round(score, 3)
                    })
            
            logger.info(f"Detected triggers: {[t['trigger'] for t in detected_triggers]}")
            
            return {
                "success": True,
                "triggers": detected_triggers
            }
            
        except Exception as e:
            logger.error(f"Trigger detection failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Singleton instance
sentiment_analyzer = SentimentAnalyzer()
