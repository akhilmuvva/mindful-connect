"""
Pytest configuration and fixtures
"""

import pytest
import os
from unittest.mock import Mock, MagicMock
from datetime import datetime

# Set test environment
os.environ['APP_ENV'] = 'testing'
os.environ['OPENAI_API_KEY'] = 'test-key'
os.environ['FIREBASE_API_KEY'] = 'test-key'
os.environ['FIREBASE_AUTH_DOMAIN'] = 'test.firebaseapp.com'
os.environ['FIREBASE_PROJECT_ID'] = 'test-project'
os.environ['FIREBASE_STORAGE_BUCKET'] = 'test.appspot.com'
os.environ['FIREBASE_MESSAGING_SENDER_ID'] = '123456'
os.environ['FIREBASE_APP_ID'] = 'test-app-id'
os.environ['FIREBASE_ADMIN_CREDENTIALS'] = './test_credentials.json'
os.environ['AES_ENCRYPTION_KEY'] = 'test_encryption_key_1234567890ab'
os.environ['SECRET_KEY'] = 'test_secret_key_minimum_32_characters_long'


@pytest.fixture
def mock_firebase_auth():
    """Mock Firebase authentication"""
    mock_auth = Mock()
    mock_auth.register_user.return_value = {
        'success': True,
        'uid': 'test-uid-123',
        'email': 'test@example.com',
        'access_token': 'test-access-token',
        'refresh_token': 'test-refresh-token'
    }
    mock_auth.login_user.return_value = {
        'success': True,
        'uid': 'test-uid-123',
        'email': 'test@example.com',
        'access_token': 'test-access-token',
        'refresh_token': 'test-refresh-token'
    }
    return mock_auth


@pytest.fixture
def mock_firestore_client():
    """Mock Firestore client"""
    mock_client = Mock()
    mock_client.create_user.return_value = True
    mock_client.get_user.return_value = {
        'uid': 'test-uid-123',
        'email': 'test@example.com',
        'created_at': datetime.utcnow()
    }
    mock_client.create_mood_entry.return_value = 'entry-id-123'
    mock_client.get_mood_entries.return_value = [
        {
            'id': 'entry-1',
            'mood_score': 7,
            'mood_label': 'good',
            'created_at': datetime.utcnow(),
            'user_id': 'test-uid-123'
        }
    ]
    return mock_client


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    mock_client = Mock()
    mock_client.generate_coping_strategies.return_value = {
        'success': True,
        'insight': 'Test coping strategy insight',
        'mood_score': 7,
        'mood_label': 'good'
    }
    mock_client.generate_mood_analysis.return_value = {
        'success': True,
        'analysis': 'Test mood analysis'
    }
    return mock_client


@pytest.fixture
def mock_sentiment_analyzer():
    """Mock sentiment analyzer"""
    mock_analyzer = Mock()
    mock_analyzer.analyze_text.return_value = {
        'success': True,
        'sentiment': 'positive',
        'confidence': 0.85,
        'mood_score': 7,
        'mood_label': 'good'
    }
    return mock_analyzer


@pytest.fixture
def sample_mood_data():
    """Sample mood entry data"""
    return {
        'mood_score': 7,
        'mood_label': 'good',
        'triggers': ['work stress'],
        'journal_text': 'Had a productive day at work today.',
        'created_at': datetime.utcnow()
    }


@pytest.fixture
def sample_user_data():
    """Sample user data"""
    return {
        'uid': 'test-uid-123',
        'email': 'test@example.com',
        'display_name': 'Test User',
        'created_at': datetime.utcnow()
    }


@pytest.fixture
def mood_history():
    """Sample mood history"""
    return [
        {'mood_score': 7, 'created_at': datetime.utcnow() - timedelta(days=i)}
        for i in range(30)
    ]


# Configure pytest
def pytest_configure(config):
    """Pytest configuration"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
