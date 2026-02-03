"""
Configuration Management for Mindful Connect
Loads and validates environment variables
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseSettings, validator
import logging

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application
    APP_ENV: str = "development"
    APP_NAME: str = "Mindful Connect"
    APP_VERSION: str = "1.0.0"
    SECRET_KEY: str
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_TIMEOUT: int = 60
    
    # Firebase
    FIREBASE_API_KEY: str
    FIREBASE_AUTH_DOMAIN: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_STORAGE_BUCKET: str
    FIREBASE_MESSAGING_SENDER_ID: str
    FIREBASE_APP_ID: str
    FIREBASE_MEASUREMENT_ID: Optional[str] = None
    FIREBASE_ADMIN_CREDENTIALS: str = "./serviceAccountKey.json"
    
    # Encryption
    AES_ENCRYPTION_KEY: str
    AES_IV_KEY: Optional[str] = None
    
    # Sentry
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: str = "development"
    SENTRY_TRACES_SAMPLE_RATE: float = 1.0
    
    # Wearable APIs
    FITBIT_CLIENT_ID: Optional[str] = None
    FITBIT_CLIENT_SECRET: Optional[str] = None
    FITBIT_REDIRECT_URI: Optional[str] = None
    APPLE_HEALTH_API_KEY: Optional[str] = None
    
    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    JWT_REFRESH_EXPIRATION_DAYS: int = 30
    
    # Database Collections
    FIRESTORE_COLLECTION_USERS: str = "users"
    FIRESTORE_COLLECTION_MOODS: str = "mood_entries"
    FIRESTORE_COLLECTION_INSIGHTS: str = "insights"
    FIRESTORE_COLLECTION_PROMPTS: str = "daily_prompts"
    FIRESTORE_COLLECTION_SESSIONS: str = "chat_sessions"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Notifications
    ENABLE_NOTIFICATIONS: bool = True
    NOTIFICATION_TIME_DEFAULT: str = "09:00"
    NOTIFICATION_TIMEZONE: str = "UTC"
    
    # ML Models
    SENTIMENT_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
    MOOD_PREDICTION_LOOKBACK_DAYS: int = 30
    MOOD_PREDICTION_FORECAST_DAYS: int = 7
    
    # Cache
    CACHE_TTL_SECONDS: int = 3600
    ENABLE_REDIS_CACHE: bool = False
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Privacy & Compliance
    ENABLE_GDPR_MODE: bool = True
    ENABLE_HIPAA_MODE: bool = True
    DATA_RETENTION_DAYS: int = 365
    ANONYMIZE_DATA: bool = True
    
    # Feature Flags
    ENABLE_WEARABLE_INTEGRATION: bool = True
    ENABLE_CHAT_THERAPY: bool = True
    ENABLE_MOOD_PREDICTION: bool = True
    ENABLE_SOCIAL_LOGIN: bool = True
    
    # API Timeouts
    API_TIMEOUT: int = 30
    
    # Streamlit
    STREAMLIT_SERVER_PORT: int = 8501
    STREAMLIT_SERVER_ADDRESS: str = "localhost"
    STREAMLIT_THEME: str = "dark"
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("AES_ENCRYPTION_KEY")
    def validate_encryption_key(cls, v):
        if len(v) != 32:
            raise ValueError("AES_ENCRYPTION_KEY must be exactly 32 characters")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    print("Please ensure .env file is properly configured")
    raise


# Configure logging
def setup_logging():
    """Configure application logging"""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('mindful_connect.log')
        ]
    )
    
    # Suppress noisy loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('transformers').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)


logger = setup_logging()


# Firebase configuration dictionary
FIREBASE_CONFIG = {
    "apiKey": settings.FIREBASE_API_KEY,
    "authDomain": settings.FIREBASE_AUTH_DOMAIN,
    "projectId": settings.FIREBASE_PROJECT_ID,
    "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
    "messagingSenderId": settings.FIREBASE_MESSAGING_SENDER_ID,
    "appId": settings.FIREBASE_APP_ID,
    "measurementId": settings.FIREBASE_MEASUREMENT_ID,
    "databaseURL": f"https://{settings.FIREBASE_PROJECT_ID}.firebaseio.com"
}


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# Export settings
__all__ = ['settings', 'logger', 'FIREBASE_CONFIG', 'BASE_DIR', 'DATA_DIR', 'MODELS_DIR', 'LOGS_DIR']
