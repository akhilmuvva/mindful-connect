"""
Firestore Database Client
Handles all database operations with encryption
"""

import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from src.config import settings
from src.database.encryption import encrypt_sensitive_data, decrypt_sensitive_data
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FirestoreClient:
    """Firestore database operations with encryption"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'db'):
            self.db = firestore.client()
            logger.info("Firestore client initialized")
    
    def _anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymize sensitive data for GDPR/HIPAA compliance
        
        Args:
            data: Original data
            
        Returns:
            Anonymized data
        """
        if not settings.ANONYMIZE_DATA:
            return data
        
        anonymized = data.copy()
        
        # Remove or hash PII
        sensitive_fields = ['email', 'phone', 'address', 'full_name']
        for field in sensitive_fields:
            if field in anonymized:
                anonymized[field] = f"***{field}***"
        
        return anonymized
    
    # User Operations
    def create_user(self, uid: str, user_data: Dict[str, Any]) -> bool:
        """
        Create user document
        
        Args:
            uid: User ID
            user_data: User information
            
        Returns:
            Success status
        """
        try:
            # Add timestamps
            user_data['created_at'] = datetime.utcnow()
            user_data['updated_at'] = datetime.utcnow()
            user_data['last_active'] = datetime.utcnow()
            
            # Encrypt sensitive fields
            if 'journal_entries' in user_data:
                user_data['journal_entries'] = encrypt_sensitive_data(user_data['journal_entries'])
            
            # Store in Firestore
            self.db.collection(settings.FIRESTORE_COLLECTION_USERS).document(uid).set(user_data)
            
            logger.info(f"User created: {uid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create user {uid}: {e}")
            return False
    
    def get_user(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Get user document
        
        Args:
            uid: User ID
            
        Returns:
            User data or None
        """
        try:
            doc = self.db.collection(settings.FIRESTORE_COLLECTION_USERS).document(uid).get()
            
            if doc.exists:
                user_data = doc.to_dict()
                
                # Decrypt sensitive fields
                if 'journal_entries' in user_data:
                    try:
                        user_data['journal_entries'] = decrypt_sensitive_data(user_data['journal_entries'])
                    except:
                        pass
                
                return user_data
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get user {uid}: {e}")
            return None
    
    def update_user(self, uid: str, update_data: Dict[str, Any]) -> bool:
        """
        Update user document
        
        Args:
            uid: User ID
            update_data: Data to update
            
        Returns:
            Success status
        """
        try:
            update_data['updated_at'] = datetime.utcnow()
            
            self.db.collection(settings.FIRESTORE_COLLECTION_USERS).document(uid).update(update_data)
            
            logger.info(f"User updated: {uid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update user {uid}: {e}")
            return False
    
    def delete_user(self, uid: str) -> bool:
        """
        Delete user document and all related data
        
        Args:
            uid: User ID
            
        Returns:
            Success status
        """
        try:
            # Delete user document
            self.db.collection(settings.FIRESTORE_COLLECTION_USERS).document(uid).delete()
            
            # Delete mood entries
            mood_entries = self.db.collection(settings.FIRESTORE_COLLECTION_MOODS)\
                .where(filter=FieldFilter('user_id', '==', uid)).stream()
            
            for entry in mood_entries:
                entry.reference.delete()
            
            # Delete insights
            insights = self.db.collection(settings.FIRESTORE_COLLECTION_INSIGHTS)\
                .where(filter=FieldFilter('user_id', '==', uid)).stream()
            
            for insight in insights:
                insight.reference.delete()
            
            # Delete chat sessions
            sessions = self.db.collection(settings.FIRESTORE_COLLECTION_SESSIONS)\
                .where(filter=FieldFilter('user_id', '==', uid)).stream()
            
            for session in sessions:
                session.reference.delete()
            
            logger.info(f"User and related data deleted: {uid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete user {uid}: {e}")
            return False
    
    # Mood Entry Operations
    def create_mood_entry(self, uid: str, mood_data: Dict[str, Any]) -> Optional[str]:
        """
        Create mood entry
        
        Args:
            uid: User ID
            mood_data: Mood entry data
            
        Returns:
            Entry ID or None
        """
        try:
            mood_data['user_id'] = uid
            mood_data['created_at'] = datetime.utcnow()
            
            # Encrypt journal text if present
            if 'journal_text' in mood_data:
                mood_data['journal_text'] = encrypt_sensitive_data(mood_data['journal_text'])
            
            # Add to Firestore
            doc_ref = self.db.collection(settings.FIRESTORE_COLLECTION_MOODS).add(mood_data)
            entry_id = doc_ref[1].id
            
            logger.info(f"Mood entry created for user {uid}: {entry_id}")
            return entry_id
            
        except Exception as e:
            logger.error(f"Failed to create mood entry for {uid}: {e}")
            return None
    
    def get_mood_entries(self, uid: str, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Get user's mood entries
        
        Args:
            uid: User ID
            limit: Maximum number of entries
            
        Returns:
            List of mood entries
        """
        try:
            entries = self.db.collection(settings.FIRESTORE_COLLECTION_MOODS)\
                .where(filter=FieldFilter('user_id', '==', uid))\
                .order_by('created_at', direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .stream()
            
            mood_entries = []
            for entry in entries:
                entry_data = entry.to_dict()
                entry_data['id'] = entry.id
                
                # Decrypt journal text
                if 'journal_text' in entry_data:
                    try:
                        entry_data['journal_text'] = decrypt_sensitive_data(entry_data['journal_text'])
                    except:
                        pass
                
                mood_entries.append(entry_data)
            
            return mood_entries
            
        except Exception as e:
            logger.error(f"Failed to get mood entries for {uid}: {e}")
            return []
    
    # Insights Operations
    def save_insight(self, uid: str, insight_data: Dict[str, Any]) -> Optional[str]:
        """
        Save AI-generated insight
        
        Args:
            uid: User ID
            insight_data: Insight data
            
        Returns:
            Insight ID or None
        """
        try:
            insight_data['user_id'] = uid
            insight_data['created_at'] = datetime.utcnow()
            
            doc_ref = self.db.collection(settings.FIRESTORE_COLLECTION_INSIGHTS).add(insight_data)
            insight_id = doc_ref[1].id
            
            logger.info(f"Insight saved for user {uid}: {insight_id}")
            return insight_id
            
        except Exception as e:
            logger.error(f"Failed to save insight for {uid}: {e}")
            return None
    
    def get_insights(self, uid: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's insights
        
        Args:
            uid: User ID
            limit: Maximum number of insights
            
        Returns:
            List of insights
        """
        try:
            insights = self.db.collection(settings.FIRESTORE_COLLECTION_INSIGHTS)\
                .where(filter=FieldFilter('user_id', '==', uid))\
                .order_by('created_at', direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .stream()
            
            insight_list = []
            for insight in insights:
                insight_data = insight.to_dict()
                insight_data['id'] = insight.id
                insight_list.append(insight_data)
            
            return insight_list
            
        except Exception as e:
            logger.error(f"Failed to get insights for {uid}: {e}")
            return []
    
    # Chat Session Operations
    def create_chat_session(self, uid: str, session_data: Dict[str, Any]) -> Optional[str]:
        """
        Create chat therapy session
        
        Args:
            uid: User ID
            session_data: Session data
            
        Returns:
            Session ID or None
        """
        try:
            session_data['user_id'] = uid
            session_data['created_at'] = datetime.utcnow()
            session_data['updated_at'] = datetime.utcnow()
            
            # Encrypt messages
            if 'messages' in session_data:
                encrypted_messages = []
                for msg in session_data['messages']:
                    if 'content' in msg:
                        msg['content'] = encrypt_sensitive_data(msg['content'])
                    encrypted_messages.append(msg)
                session_data['messages'] = encrypted_messages
            
            doc_ref = self.db.collection(settings.FIRESTORE_COLLECTION_SESSIONS).add(session_data)
            session_id = doc_ref[1].id
            
            logger.info(f"Chat session created for user {uid}: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to create chat session for {uid}: {e}")
            return None
    
    def update_chat_session(self, session_id: str, messages: List[Dict[str, Any]]) -> bool:
        """
        Update chat session with new messages
        
        Args:
            session_id: Session ID
            messages: List of messages
            
        Returns:
            Success status
        """
        try:
            # Encrypt messages
            encrypted_messages = []
            for msg in messages:
                if 'content' in msg:
                    msg['content'] = encrypt_sensitive_data(msg['content'])
                encrypted_messages.append(msg)
            
            self.db.collection(settings.FIRESTORE_COLLECTION_SESSIONS).document(session_id).update({
                'messages': encrypted_messages,
                'updated_at': datetime.utcnow()
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update chat session {session_id}: {e}")
            return False
    
    def get_chat_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get chat session
        
        Args:
            session_id: Session ID
            
        Returns:
            Session data or None
        """
        try:
            doc = self.db.collection(settings.FIRESTORE_COLLECTION_SESSIONS).document(session_id).get()
            
            if doc.exists:
                session_data = doc.to_dict()
                
                # Decrypt messages
                if 'messages' in session_data:
                    decrypted_messages = []
                    for msg in session_data['messages']:
                        if 'content' in msg:
                            try:
                                msg['content'] = decrypt_sensitive_data(msg['content'])
                            except:
                                pass
                        decrypted_messages.append(msg)
                    session_data['messages'] = decrypted_messages
                
                return session_data
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get chat session {session_id}: {e}")
            return None


# Singleton instance
firestore_client = FirestoreClient()
