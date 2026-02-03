"""
Database initialization script
Creates necessary Firestore collections and indexes
"""

import firebase_admin
from firebase_admin import credentials, firestore
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_firestore():
    """Initialize Firestore database with collections and indexes"""
    
    try:
        # Initialize Firebase Admin
        cred_path = Path(__file__).parent.parent / "serviceAccountKey.json"
        
        if not cred_path.exists():
            logger.error(f"Service account key not found at {cred_path}")
            logger.info("Please download your Firebase service account key and place it in the project root")
            return False
        
        cred = credentials.Certificate(str(cred_path))
        firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        
        logger.info("Initializing Firestore collections...")
        
        # Create sample documents to initialize collections
        collections = {
            'users': {
                '_init': {
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'description': 'User profiles and settings'
                }
            },
            'mood_entries': {
                '_init': {
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'description': 'Daily mood logs'
                }
            },
            'insights': {
                '_init': {
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'description': 'AI-generated insights'
                }
            },
            'daily_prompts': {
                '_init': {
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'description': 'Daily mindfulness prompts'
                }
            },
            'chat_sessions': {
                '_init': {
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'description': 'AI therapy chat sessions'
                }
            }
        }
        
        for collection_name, docs in collections.items():
            for doc_id, doc_data in docs.items():
                db.collection(collection_name).document(doc_id).set(doc_data)
                logger.info(f"Created collection: {collection_name}")
        
        logger.info("✅ Firestore initialization complete!")
        logger.info("\nNext steps:")
        logger.info("1. Set up Firestore indexes in Firebase Console")
        logger.info("2. Configure security rules")
        logger.info("3. Enable Firebase Authentication")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Firestore: {e}")
        return False


if __name__ == "__main__":
    initialize_firestore()
