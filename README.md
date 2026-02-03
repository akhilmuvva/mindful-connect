# Mindful Connect - AI-Powered Mental Wellness Companion

A comprehensive, production-ready mental wellness application that combines AI-powered insights, mood tracking, personalized coping strategies, and advanced features like wearable integration and predictive analytics.

## 🌟 Features

### Core Features
- **User Authentication**: Email/password, Google OAuth, JWT tokens
- **Mood Tracking**: Daily logging via interactive forms and sliders
- **Sentiment Analysis**: NLP-powered mood analysis using Hugging Face Transformers
- **Personalized Insights**: AI-generated coping strategies using OpenAI GPT-4o
- **Mood Trends**: Interactive charts with Matplotlib and Plotly
- **Daily Prompts**: Scheduled mindfulness exercises and journaling
- **Push Notifications**: Firebase Cloud Messaging integration

### Advanced Features
- **Wearable Integration**: Fitbit and Apple Health API support for biometrics
- **AI Chat Therapy**: LangChain-powered conversational therapy simulation
- **Privacy Compliance**: GDPR/HIPAA compliant with AES-256 encryption
- **Predictive Analytics**: ML-based mood forecasting using Scikit-learn
- **Real-time Database**: Firestore for seamless data synchronization

### Technical Excellence
- **Error Handling**: Comprehensive try-except blocks throughout
- **Logging**: Sentry integration for production monitoring
- **Scalability**: Docker containerization
- **CI/CD**: GitHub Actions pipeline
- **Testing**: Pytest for unit and integration tests

## 🚀 Tech Stack

- **Backend**: Python 3.12
- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4o, Hugging Face Transformers, Scikit-learn, LangChain
- **Authentication**: Firebase Authentication
- **Database**: Cloud Firestore
- **Encryption**: AES-256
- **Testing**: Pytest
- **Deployment**: Vercel/Heroku
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry

## 📋 Prerequisites

- Python 3.12+
- Node.js 18+ (for Firebase CLI)
- Docker (optional, for containerization)
- Git
- Firebase account
- OpenAI API account
- Sentry account (for monitoring)

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd mindful-connect
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# Firebase Configuration
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_MEASUREMENT_ID=your_measurement_id

# Firebase Admin SDK (Service Account)
FIREBASE_ADMIN_CREDENTIALS=path/to/serviceAccountKey.json

# Encryption
AES_ENCRYPTION_KEY=your_32_byte_encryption_key_here

# Sentry
SENTRY_DSN=your_sentry_dsn_here

# Wearable APIs (Optional)
FITBIT_CLIENT_ID=your_fitbit_client_id
FITBIT_CLIENT_SECRET=your_fitbit_client_secret
APPLE_HEALTH_API_KEY=your_apple_health_key

# Application Settings
APP_ENV=development
SECRET_KEY=your_secret_key_for_jwt
LOG_LEVEL=INFO
```

### 5. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Authentication (Email/Password and Google)
4. Create a Firestore database
5. Download the service account key JSON file
6. Place it in the project root and update `FIREBASE_ADMIN_CREDENTIALS` in `.env`

### 6. Initialize Database

```bash
python scripts/init_database.py
```

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Run Specific Test Suites

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Authentication tests
pytest tests/test_auth.py -v

# Mood tracking tests
pytest tests/test_mood_tracker.py -v
```

### View Coverage Report

```bash
# Open htmlcov/index.html in your browser
```

## 🏃 Running the Application

### Development Mode

```bash
streamlit run src/app.py
```

The application will be available at `http://localhost:8501`

### Production Mode

```bash
streamlit run src/app.py --server.port=8080 --server.address=0.0.0.0
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t mindful-connect:latest .
```

### Run Container

```bash
docker run -p 8501:8501 --env-file .env mindful-connect:latest
```

### Docker Compose

```bash
docker-compose up -d
```

## 🚀 Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Login to Heroku:
   ```bash
   heroku login
   ```
3. Create a new app:
   ```bash
   heroku create mindful-connect-app
   ```
4. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   # Set all other environment variables
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

### Vercel Deployment

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```
2. Deploy:
   ```bash
   vercel --prod
   ```
3. Configure environment variables in Vercel dashboard

## 📊 Project Structure

```
mindful-connect/
├── src/
│   ├── app.py                      # Main Streamlit application
│   ├── config.py                   # Configuration management
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── firebase_auth.py        # Firebase authentication
│   │   └── jwt_handler.py          # JWT token management
│   ├── database/
│   │   ├── __init__.py
│   │   ├── firestore_client.py     # Firestore operations
│   │   └── encryption.py           # AES-256 encryption
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── openai_client.py        # OpenAI GPT-4o integration
│   │   ├── sentiment_analyzer.py   # Hugging Face NLP
│   │   ├── mood_predictor.py       # ML mood forecasting
│   │   └── therapy_chat.py         # LangChain chat agent
│   ├── features/
│   │   ├── __init__.py
│   │   ├── mood_tracker.py         # Mood logging and tracking
│   │   ├── insights_generator.py   # AI insights generation
│   │   ├── daily_prompts.py        # Mindfulness prompts
│   │   └── notifications.py        # Firebase Cloud Messaging
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── fitbit_api.py           # Fitbit integration
│   │   └── apple_health.py         # Apple Health integration
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── components.py           # Reusable UI components
│   │   ├── dashboard.py            # Main dashboard
│   │   ├── mood_charts.py          # Visualization components
│   │   └── chat_interface.py       # Chat UI
│   └── utils/
│       ├── __init__.py
│       ├── logger.py               # Logging configuration
│       ├── validators.py           # Input validation
│       └── helpers.py              # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration
│   ├── unit/
│   │   ├── test_auth.py
│   │   ├── test_encryption.py
│   │   ├── test_sentiment.py
│   │   └── test_mood_predictor.py
│   └── integration/
│       ├── test_user_flow.py
│       ├── test_mood_tracking.py
│       └── test_ai_insights.py
├── scripts/
│   ├── init_database.py            # Database initialization
│   └── seed_data.py                # Sample data seeding
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # GitHub Actions CI/CD
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore
├── pytest.ini                      # Pytest configuration
├── setup.sh                        # Streamlit setup script
└── README.md
```

## 🔐 Security & Privacy

- **AES-256 Encryption**: All sensitive data encrypted at rest
- **GDPR Compliance**: Data anonymization and user consent management
- **HIPAA Compliance**: Healthcare data protection standards
- **JWT Authentication**: Secure token-based authentication
- **Firebase Security Rules**: Strict database access controls
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: API request throttling
- **Audit Logging**: All actions logged for compliance

## 📈 Monitoring & Logging

- **Sentry Integration**: Real-time error tracking and performance monitoring
- **Application Logs**: Structured logging with different severity levels
- **User Analytics**: Privacy-compliant usage tracking
- **Health Checks**: Automated system health monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@mindfulconnect.com
- Documentation: https://docs.mindfulconnect.com

## 🙏 Acknowledgments

- OpenAI for GPT-4o API
- Hugging Face for Transformers
- Firebase for authentication and database
- Streamlit for the amazing UI framework
- The open-source community

---

**Built with ❤️ for mental wellness**
