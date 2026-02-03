"""
Unit tests for encryption module
"""

import pytest
from src.database.encryption import AESEncryption, encrypt_sensitive_data, decrypt_sensitive_data


class TestAESEncryption:
    """Test AES-256 encryption"""
    
    def test_encrypt_decrypt_string(self):
        """Test encrypting and decrypting a string"""
        encryption = AESEncryption()
        original_text = "This is sensitive data"
        
        encrypted = encryption.encrypt(original_text)
        decrypted = encryption.decrypt(encrypted)
        
        assert encrypted != original_text
        assert decrypted == original_text
    
    def test_encrypt_decrypt_dict(self):
        """Test encrypting and decrypting a dictionary"""
        encryption = AESEncryption()
        original_dict = {
            "journal": "My private thoughts",
            "mood": "happy",
            "score": "8"
        }
        
        encrypted_dict = encryption.encrypt_dict(original_dict)
        decrypted_dict = encryption.decrypt_dict(encrypted_dict)
        
        assert encrypted_dict['journal'] != original_dict['journal']
        assert decrypted_dict == original_dict
    
    def test_encrypt_produces_different_output(self):
        """Test that same input produces different encrypted output (due to IV)"""
        encryption = AESEncryption()
        text = "Test data"
        
        encrypted1 = encryption.encrypt(text)
        encrypted2 = encryption.encrypt(text)
        
        assert encrypted1 != encrypted2  # Different IVs
        assert encryption.decrypt(encrypted1) == text
        assert encryption.decrypt(encrypted2) == text
    
    def test_helper_functions(self):
        """Test helper encryption functions"""
        original = "Sensitive information"
        
        encrypted = encrypt_sensitive_data(original)
        decrypted = decrypt_sensitive_data(encrypted)
        
        assert decrypted == original
