"""
Unit tests for authentication module
"""

import pytest
from unittest.mock import Mock, patch
from src.auth.jwt_handler import JWTHandler


class TestJWTHandler:
    """Test JWT token handling"""
    
    def test_create_access_token(self):
        """Test access token creation"""
        handler = JWTHandler()
        token = handler.create_access_token({"uid": "test-123", "email": "test@example.com"})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        handler = JWTHandler()
        token = handler.create_refresh_token({"uid": "test-123", "email": "test@example.com"})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_valid_token(self):
        """Test verifying valid token"""
        handler = JWTHandler()
        data = {"uid": "test-123", "email": "test@example.com"}
        token = handler.create_access_token(data)
        
        payload = handler.verify_token(token)
        
        assert payload is not None
        assert payload['uid'] == "test-123"
        assert payload['email'] == "test@example.com"
        assert payload['type'] == "access"
    
    def test_verify_invalid_token(self):
        """Test verifying invalid token"""
        handler = JWTHandler()
        payload = handler.verify_token("invalid-token")
        
        assert payload is None
    
    def test_token_expiration(self):
        """Test token contains expiration"""
        handler = JWTHandler()
        token = handler.create_access_token({"uid": "test-123"})
        payload = handler.verify_token(token)
        
        assert 'exp' in payload
        assert 'iat' in payload
