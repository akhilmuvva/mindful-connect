# Mindful Connect - Setup Guide

## 🚀 Quick Start Guide

### Step 1: Clone and Setup Environment

```bash
# Navigate to project directory
cd mindful-connect

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Firebase Configuration

1. **Create Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add Project"
   - Follow the setup wizard

2. **Enable Authentication**
   - In Firebase Console, go to Authentication
   - Click "Get Started"
   - Enable "Email/Password" provider
   - Enable "Google" provider (optional)

3. **Create Firestore Database**
   - Go to Firestore Database
   - Click "Create Database"
   - Start in "Test Mode" (we'll add security rules later)
   - Choose your region

4. **Download Service Account Key**
   - Go to Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Save as `serviceAccountKey.json` in project root

5. **Get Web App Config**
   - Go to Project Settings → General
   - Scroll to "Your apps"
   - Click "Web" icon to add web app
   - Copy the config values

### Step 3: OpenAI API Setup

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (you won't see it again!)

### Step 4: Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and fill in your actual values:

```env
# OpenAI
OPENAI_API_KEY=sk-proj-your-actual-key-here
OPENAI_MODEL=gpt-4o

# Firebase (from Firebase Console)
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=your-app-id

# Encryption (generate a random 32-character key)
AES_ENCRYPTION_KEY=your_32_character_encryption_key

# JWT Secret (generate a random 32+ character key)
SECRET_KEY=your_secret_key_minimum_32_characters_long

# Sentry (optional, for production monitoring)
SENTRY_DSN=your-sentry-dsn-here
```

**Generate Encryption Keys:**
```python
import secrets
print("AES Key:", secrets.token_urlsafe(32)[:32])
print("Secret Key:", secrets.token_urlsafe(48))
```

### Step 5: Initialize Database

```bash
python scripts/init_database.py
```

### Step 6: Run the Application

```bash
streamlit run src/app.py
```

The app will open at `http://localhost:8501`

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_auth.py -v

# View coverage report
# Open htmlcov/index.html in your browser
```

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build image
docker build -t mindful-connect .

# Run container
docker run -p 8501:8501 --env-file .env mindful-connect
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🚀 Production Deployment

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create mindful-connect-app
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your-key
   heroku config:set FIREBASE_API_KEY=your-key
   # Set all other environment variables
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

3. **Configure Environment Variables**
   - Go to Vercel Dashboard
   - Select your project
   - Settings → Environment Variables
   - Add all variables from `.env`

## 🔐 Security Setup

### Firebase Security Rules

Add these rules in Firebase Console → Firestore → Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /mood_entries/{entryId} {
      allow read, write: if request.auth != null && 
                           resource.data.user_id == request.auth.uid;
    }
    
    match /insights/{insightId} {
      allow read, write: if request.auth != null && 
                           resource.data.user_id == request.auth.uid;
    }
    
    match /chat_sessions/{sessionId} {
      allow read, write: if request.auth != null && 
                           resource.data.user_id == request.auth.uid;
    }
  }
}
```

### Enable HTTPS

For production, always use HTTPS. Most platforms (Heroku, Vercel) provide this automatically.

## 📊 Monitoring Setup

### Sentry Integration

1. Create account at [sentry.io](https://sentry.io)
2. Create new project
3. Copy DSN
4. Add to `.env`:
   ```env
   SENTRY_DSN=your-sentry-dsn
   SENTRY_ENVIRONMENT=production
   ```

## 🔧 Troubleshooting

### Common Issues

**Issue: Firebase initialization fails**
- Ensure `serviceAccountKey.json` is in the correct location
- Check file permissions
- Verify Firebase project ID matches

**Issue: OpenAI API errors**
- Verify API key is correct
- Check API quota/billing
- Ensure you have GPT-4o access

**Issue: Import errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.12+ required)

**Issue: Streamlit won't start**
- Check if port 8501 is already in use
- Try: `streamlit run src/app.py --server.port=8502`

### Getting Help

- Check logs in `logs/mindful_connect.log`
- Review Sentry dashboard for errors
- Check Firebase Console for authentication issues

## 📝 Development Workflow

### Adding New Features

1. Create feature branch
   ```bash
   git checkout -b feature/new-feature
   ```

2. Make changes and test
   ```bash
   pytest tests/ -v
   ```

3. Commit and push
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/new-feature
   ```

4. Create Pull Request on GitHub

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
flake8 src/ tests/
```

## 🎯 Next Steps

1. ✅ Complete Firebase setup
2. ✅ Configure environment variables
3. ✅ Run initial tests
4. ✅ Deploy to production
5. 📱 Set up mobile notifications (Firebase Cloud Messaging)
6. 🔗 Integrate wearable APIs (Fitbit/Apple Health)
7. 📊 Set up analytics dashboard
8. 🤖 Fine-tune AI prompts based on user feedback

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Firebase Documentation](https://firebase.google.com/docs)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)

---

**Need help?** Open an issue on GitHub or contact support@mindfulconnect.com
