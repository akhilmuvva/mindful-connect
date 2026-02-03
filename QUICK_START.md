# 🚀 Mindful Connect - Quick Start Guide

## ✅ What's Done

1. ✅ **Repository pushed to GitHub**: https://github.com/akhilmuvva/mindful-connect
2. ✅ **Virtual environment created**: `venv` folder
3. ✅ **Core dependencies installed**: Streamlit, OpenAI, Firebase, PyTorch, etc.
4. ✅ **Environment file created**: `.env` (needs configuration)

## 🎯 Next Steps to Run the App

### Step 1: Configure API Keys (REQUIRED)

You need to set up two services:

#### A. Firebase Setup (10 minutes)
1. Go to https://console.firebase.google.com/
2. Click "Add Project" → Name it "Mindful Connect"
3. **Enable Authentication**:
   - Click "Authentication" → "Get Started"
   - Enable "Email/Password" provider
4. **Create Firestore Database**:
   - Click "Firestore Database" → "Create Database"
   - Choose "Start in test mode"
   - Select your region
5. **Get Service Account Key**:
   - Click gear icon → "Project Settings"
   - Go to "Service Accounts" tab
   - Click "Generate New Private Key"
   - Save as `serviceAccountKey.json` in project root
6. **Get Web App Config**:
   - In "Project Settings" → "General" tab
   - Click "</>" (web) icon → Register app
   - Copy the config values

#### B. OpenAI API Key (5 minutes)
1. Go to https://platform.openai.com/
2. Sign up/login
3. Click profile → "View API Keys"
4. Click "Create new secret key"
5. Copy the key immediately!

### Step 2: Update .env File

Open `.env` file and update these values:

```env
# OpenAI (from Step 1B)
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE

# Firebase (from Step 1A - Web App Config)
FIREBASE_API_KEY=AIzaSy...
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abc123

# Firebase Admin (from Step 1A)
FIREBASE_ADMIN_CREDENTIALS=./serviceAccountKey.json

# Generate secure keys (see below)
AES_ENCRYPTION_KEY=your_32_character_key_here_12345
SECRET_KEY=your_secret_key_minimum_32_characters
```

#### Generate Encryption Keys

Run this in PowerShell:
```powershell
.\venv\Scripts\activate
python -c "import secrets; print('AES_ENCRYPTION_KEY=' + secrets.token_urlsafe(32)[:32]); print('SECRET_KEY=' + secrets.token_urlsafe(48))"
```

Copy the output to your `.env` file.

### Step 3: Initialize Database (Optional)

```powershell
.\venv\Scripts\activate
python scripts/init_database.py
```

### Step 4: Run the App! 🎉

```powershell
.\venv\Scripts\activate
streamlit run src/app.py
```

The app will open at: **http://localhost:8501**

## 📱 Using the App

1. **Sign Up**: Create an account with email/password
2. **Log Mood**: Click "📝 Log Mood" → Rate your mood → Add notes
3. **View Dashboard**: See mood trends, AI insights, and predictions
4. **Get Insights**: AI will analyze your mood and provide personalized coping strategies

## 🐛 Troubleshooting

### "Firebase initialization failed"
- Make sure `serviceAccountKey.json` is in the project root
- Check that all Firebase config values in `.env` are correct

### "OpenAI API error"
- Verify your API key in `.env`
- Check you have credits in your OpenAI account
- You can change model to `gpt-3.5-turbo` if you don't have GPT-4 access

### "Module not found"
```powershell
.\venv\Scripts\activate
pip install -r requirements-core.txt
```

### Port already in use
```powershell
streamlit run src/app.py --server.port=8502
```

## 📚 Project Structure

```
mindful-connect/
├── src/
│   ├── app.py              # Main Streamlit app (START HERE)
│   ├── config.py           # Configuration
│   ├── auth/               # Authentication
│   ├── database/           # Firestore & encryption
│   ├── ai/                 # OpenAI, sentiment analysis
│   └── utils/              # Logging, helpers
├── .env                    # Your API keys (CONFIGURE THIS)
├── serviceAccountKey.json  # Firebase credentials (ADD THIS)
└── requirements-core.txt   # Dependencies (INSTALLED)
```

## 🎯 Quick Commands Reference

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run the app
streamlit run src/app.py

# Install more packages
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Deactivate virtual environment
deactivate
```

## 🌟 Features Available

✅ User authentication (email/password)
✅ Mood tracking with AI analysis
✅ Sentiment analysis using Hugging Face
✅ Personalized insights from GPT-4
✅ Mood trend visualization
✅ Predictive mood forecasting
✅ Secure encrypted data storage
✅ Beautiful modern UI

## 🚀 What's Next?

After getting the app running:
1. Log several mood entries to see trends
2. Explore the AI insights
3. Check mood predictions
4. Customize the UI in `src/app.py`
5. Deploy to production (see SETUP_GUIDE.md)

## 📞 Need Help?

- Check `GETTING_STARTED.md` for detailed setup
- Review `SETUP_GUIDE.md` for deployment
- See `PROJECT_OVERVIEW.md` for features
- Check logs in `logs/` folder

---

**You're almost there! Just configure Firebase & OpenAI, then run the app!** 🎉

**Current Status**: ✅ Code ready | ✅ Dependencies installed | ⏳ Needs API configuration
