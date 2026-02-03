"""
Firebase Authentication Module
Handles user registration, login, and JWT token management
"""

import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta

from src.config import settings, FIREBASE_CONFIG
from src.auth.jwt_handler import JWTHandler
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FirebaseAuth:
    """Firebase authentication manager"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_firebase()
            self._initialized = True
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK and Pyrebase"""
        try:
            # Initialize Firebase Admin SDK
            if not firebase_admin._apps:
                cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialized successfully")
            
            # Initialize Pyrebase for client-side operations
            self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
            self.auth_client = self.firebase.auth()
            
            # Initialize JWT handler
            self.jwt_handler = JWTHandler()
            
            logger.info("Firebase authentication initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            raise
    
    def register_user(self, email: str, password: str, display_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Register a new user with email and password
        
        Args:
            email: User email address
            password: User password
            display_name: Optional display name
            
        Returns:
            Dictionary with user info and tokens
        """
        try:
            # Create user with Pyrebase
            user = self.auth_client.create_user_with_email_and_password(email, password)
            
            # Update profile if display name provided
            if display_name:
                self.auth_client.update_profile(user['idToken'], display_name=display_name)
            
            # Send email verification
            self.auth_client.send_email_verification(user['idToken'])
            
            # Create custom JWT token
            uid = user['localId']
            custom_token = self.jwt_handler.create_access_token(
                data={"uid": uid, "email": email}
            )
            refresh_token = self.jwt_handler.create_refresh_token(
                data={"uid": uid, "email": email}
            )
            
            logger.info(f"User registered successfully: {email}")
            
            return {
                "success": True,
                "uid": uid,
                "email": email,
                "display_name": display_name,
                "access_token": custom_token,
                "refresh_token": refresh_token,
                "firebase_token": user['idToken'],
                "message": "Registration successful. Please verify your email."
            }
            
        except Exception as e:
            logger.error(f"Registration failed for {email}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Registration failed. Please try again."
            }
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login user with email and password
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            Dictionary with user info and tokens
        """
        try:
            # Sign in with Pyrebase
            user = self.auth_client.sign_in_with_email_and_password(email, password)
            
            # Get user info
            account_info = self.auth_client.get_account_info(user['idToken'])
            user_data = account_info['users'][0]
            
            # Check if email is verified
            email_verified = user_data.get('emailVerified', False)
            
            # Create custom JWT tokens
            uid = user['localId']
            custom_token = self.jwt_handler.create_access_token(
                data={"uid": uid, "email": email}
            )
            refresh_token = self.jwt_handler.create_refresh_token(
                data={"uid": uid, "email": email}
            )
            
            logger.info(f"User logged in successfully: {email}")
            
            return {
                "success": True,
                "uid": uid,
                "email": email,
                "display_name": user_data.get('displayName'),
                "email_verified": email_verified,
                "access_token": custom_token,
                "refresh_token": refresh_token,
                "firebase_token": user['idToken'],
                "message": "Login successful"
            }
            
        except Exception as e:
            logger.error(f"Login failed for {email}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Login failed. Please check your credentials."
            }
    
    def login_with_google(self, id_token: str) -> Dict[str, Any]:
        """
        Login user with Google OAuth
        
        Args:
            id_token: Google ID token
            
        Returns:
            Dictionary with user info and tokens
        """
        try:
            # Verify the Google ID token
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            
            # Get or create user
            try:
                user = auth.get_user(uid)
            except auth.UserNotFoundError:
                user = auth.create_user(
                    uid=uid,
                    email=email,
                    email_verified=True
                )
            
            # Create custom JWT tokens
            custom_token = self.jwt_handler.create_access_token(
                data={"uid": uid, "email": email}
            )
            refresh_token = self.jwt_handler.create_refresh_token(
                data={"uid": uid, "email": email}
            )
            
            logger.info(f"User logged in with Google: {email}")
            
            return {
                "success": True,
                "uid": uid,
                "email": email,
                "display_name": user.display_name,
                "email_verified": True,
                "access_token": custom_token,
                "refresh_token": refresh_token,
                "message": "Google login successful"
            }
            
        except Exception as e:
            logger.error(f"Google login failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Google login failed. Please try again."
            }
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token
        
        Args:
            token: JWT token to verify
            
        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = self.jwt_handler.verify_token(token)
            return payload
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            New access and refresh tokens or None
        """
        try:
            payload = self.jwt_handler.verify_token(refresh_token)
            
            if payload:
                # Create new tokens
                new_access_token = self.jwt_handler.create_access_token(
                    data={"uid": payload['uid'], "email": payload['email']}
                )
                new_refresh_token = self.jwt_handler.create_refresh_token(
                    data={"uid": payload['uid'], "email": payload['email']}
                )
                
                return {
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            return None
    
    def reset_password(self, email: str) -> Dict[str, Any]:
        """
        Send password reset email
        
        Args:
            email: User email address
            
        Returns:
            Success status and message
        """
        try:
            self.auth_client.send_password_reset_email(email)
            logger.info(f"Password reset email sent to: {email}")
            
            return {
                "success": True,
                "message": "Password reset email sent. Please check your inbox."
            }
            
        except Exception as e:
            logger.error(f"Password reset failed for {email}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send password reset email."
            }
    
    def update_profile(self, uid: str, display_name: Optional[str] = None, 
                      photo_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Update user profile
        
        Args:
            uid: User ID
            display_name: New display name
            photo_url: New photo URL
            
        Returns:
            Success status and message
        """
        try:
            update_data = {}
            if display_name:
                update_data['display_name'] = display_name
            if photo_url:
                update_data['photo_url'] = photo_url
            
            auth.update_user(uid, **update_data)
            logger.info(f"Profile updated for user: {uid}")
            
            return {
                "success": True,
                "message": "Profile updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Profile update failed for {uid}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update profile"
            }
    
    def delete_user(self, uid: str) -> Dict[str, Any]:
        """
        Delete user account
        
        Args:
            uid: User ID
            
        Returns:
            Success status and message
        """
        try:
            auth.delete_user(uid)
            logger.info(f"User deleted: {uid}")
            
            return {
                "success": True,
                "message": "Account deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"User deletion failed for {uid}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete account"
            }
    
    def get_user(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Get user information
        
        Args:
            uid: User ID
            
        Returns:
            User information or None
        """
        try:
            user = auth.get_user(uid)
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "photo_url": user.photo_url,
                "email_verified": user.email_verified,
                "disabled": user.disabled,
                "created_at": user.user_metadata.creation_timestamp,
                "last_sign_in": user.user_metadata.last_sign_in_timestamp
            }
        except Exception as e:
            logger.error(f"Failed to get user {uid}: {e}")
            return None


# Singleton instance
firebase_auth = FirebaseAuth()
