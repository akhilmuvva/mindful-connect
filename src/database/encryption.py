"""
AES-256 Encryption Module
Handles encryption and decryption of sensitive data
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
from typing import Union
import logging

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AESEncryption:
    """AES-256 encryption handler"""
    
    def __init__(self):
        # Ensure key is 32 bytes for AES-256
        self.key = settings.AES_ENCRYPTION_KEY.encode('utf-8')[:32]
        if len(self.key) < 32:
            self.key = self.key.ljust(32, b'0')
        
        self.block_size = AES.block_size
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using AES-256-CBC
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Base64 encoded encrypted text
        """
        try:
            # Generate random IV
            iv = get_random_bytes(self.block_size)
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            # Pad and encrypt
            padded_data = pad(plaintext.encode('utf-8'), self.block_size)
            ciphertext = cipher.encrypt(padded_data)
            
            # Combine IV and ciphertext, then base64 encode
            encrypted_data = iv + ciphertext
            encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
            
            return encoded_data
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt encrypted text using AES-256-CBC
        
        Args:
            encrypted_text: Base64 encoded encrypted text
            
        Returns:
            Decrypted plaintext
        """
        try:
            # Base64 decode
            encrypted_data = base64.b64decode(encrypted_text.encode('utf-8'))
            
            # Extract IV and ciphertext
            iv = encrypted_data[:self.block_size]
            ciphertext = encrypted_data[self.block_size:]
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            # Decrypt and unpad
            padded_plaintext = cipher.decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, self.block_size)
            
            return plaintext.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def encrypt_dict(self, data: dict) -> dict:
        """
        Encrypt dictionary values
        
        Args:
            data: Dictionary with string values
            
        Returns:
            Dictionary with encrypted values
        """
        try:
            encrypted_data = {}
            for key, value in data.items():
                if isinstance(value, str):
                    encrypted_data[key] = self.encrypt(value)
                else:
                    encrypted_data[key] = value
            return encrypted_data
        except Exception as e:
            logger.error(f"Dictionary encryption failed: {e}")
            raise
    
    def decrypt_dict(self, encrypted_data: dict) -> dict:
        """
        Decrypt dictionary values
        
        Args:
            encrypted_data: Dictionary with encrypted values
            
        Returns:
            Dictionary with decrypted values
        """
        try:
            decrypted_data = {}
            for key, value in encrypted_data.items():
                if isinstance(value, str):
                    try:
                        decrypted_data[key] = self.decrypt(value)
                    except:
                        # If decryption fails, assume it wasn't encrypted
                        decrypted_data[key] = value
                else:
                    decrypted_data[key] = value
            return decrypted_data
        except Exception as e:
            logger.error(f"Dictionary decryption failed: {e}")
            raise


# Singleton instance
encryption = AESEncryption()


def encrypt_sensitive_data(data: Union[str, dict]) -> Union[str, dict]:
    """
    Encrypt sensitive data
    
    Args:
        data: String or dictionary to encrypt
        
    Returns:
        Encrypted data
    """
    if isinstance(data, str):
        return encryption.encrypt(data)
    elif isinstance(data, dict):
        return encryption.encrypt_dict(data)
    else:
        raise ValueError("Data must be string or dictionary")


def decrypt_sensitive_data(encrypted_data: Union[str, dict]) -> Union[str, dict]:
    """
    Decrypt sensitive data
    
    Args:
        encrypted_data: Encrypted string or dictionary
        
    Returns:
        Decrypted data
    """
    if isinstance(encrypted_data, str):
        return encryption.decrypt(encrypted_data)
    elif isinstance(encrypted_data, dict):
        return encryption.decrypt_dict(encrypted_data)
    else:
        raise ValueError("Encrypted data must be string or dictionary")
