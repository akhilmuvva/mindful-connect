"""Database module initialization"""

from src.database.firestore_client import firestore_client, FirestoreClient
from src.database.encryption import encryption, encrypt_sensitive_data, decrypt_sensitive_data

__all__ = [
    'firestore_client',
    'FirestoreClient',
    'encryption',
    'encrypt_sensitive_data',
    'decrypt_sensitive_data'
]
