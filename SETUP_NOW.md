# 🔧 SETUP INSTRUCTIONS - READ THIS FIRST!

## ✅ What's Already Done

1. ✅ Virtual environment created (`venv`)
2. ✅ Core dependencies installed
3. ✅ Encryption keys generated and configured
4. ✅ `.env` file created with secure keys

---

## ⚠️ REQUIRED: API Keys Setup

Your app needs **2 API keys** to work. Follow these steps:

---

## 🔥 Step 1: Firebase Setup (10 minutes)

### A. Create Firebase Project

1. **Go to**: https://console.firebase.google.com/
2. **Click**: "Add Project" or "Create a project"
3. **Project name**: `mindful-connect` (or any name you like)
4. **Google Analytics**: Disable (optional, not needed)
5. **Click**: "Create Project"
6. **Wait** for project creation to complete

### B. Enable Authentication

1. In your Firebase project, click **"Authentication"** in the left sidebar
2. Click **"Get Started"**
3. Click **"Email/Password"** under "Sign-in method"
4. **Toggle ON** the "Email/Password" switch
5. Click **"Save"**

### C. Create Firestore Database

1. Click **"Firestore Database"** in the left sidebar
2. Click **"Create database"**
3. **Select**: "Start in test mode" (we'll secure it later)
4. **Choose region**: Select the closest region to you
5. Click **"Enable"**
6. Wait for database creation

### D. Get Service Account Key (IMPORTANT!)

1. Click the **⚙️ gear icon** → **"Project settings"**
2. Go to **"Service accounts"** tab
3. Click **"Generate new private key"**
4. Click **"Generate key"** in the popup
5. A JSON file will download
6. **IMPORTANT**: Rename it to `serviceAccountKey.json`
7. **IMPORTANT**: Move it to your project root folder:
   ```
   C:\Users\akhil\.gemini\antigravity\scratch\mindful-connect\serviceAccountKey.json
   ```

### E. Get Web App Configuration

1. Still in **"Project settings"** → Go to **"General"** tab
2. Scroll down to **"Your apps"**
3. Click the **"</>"** (web) icon
4. **App nickname**: `Mindful Connect Web`
5. **DO NOT** check "Also set up Firebase Hosting"
6. Click **"Register app"**
7. You'll see a `firebaseConfig` object. **Copy these values**:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",              // ← Copy this
  authDomain: "your-project.firebaseapp.com",  // ← Copy this
  projectId: "your-project-id",     // ← Copy this
  storageBucket: "your-project.appspot.com",   // ← Copy this
  messagingSenderId: "123456789",   // ← Copy this
  appId: "1:123456789:web:abc123"   // ← Copy this
};
```

8. **Open** your `.env` file and update these lines:

```env
FIREBASE_API_KEY=AIzaSy...  # Paste apiKey here
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com  # Paste authDomain
FIREBASE_PROJECT_ID=your-project-id  # Paste projectId
FIREBASE_STORAGE_BUCKET=your-project.appspot.com  # Paste storageBucket
FIREBASE_MESSAGING_SENDER_ID=123456789  # Paste messagingSenderId
FIREBASE_APP_ID=1:123456789:web:abc123  # Paste appId
```

---

## 🤖 Step 2: OpenAI API Key (5 minutes)

### A. Create OpenAI Account & Get API Key

1. **Go to**: https://platform.openai.com/
2. **Sign up** or **Log in**
3. Click your **profile icon** (top right) → **"View API keys"**
4. Click **"+ Create new secret key"**
5. **Name**: `Mindful Connect`
6. Click **"Create secret key"**
7. **COPY THE KEY IMMEDIATELY** (you won't see it again!)
   - It looks like: `sk-proj-abc123...`

### B. Add to .env File

1. **Open** your `.env` file
2. **Find** this line:
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
3. **Replace** with your actual key:
   ```env
   OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
   ```

### C. Add Billing (REQUIRED!)

⚠️ **IMPORTANT**: OpenAI requires billing to be set up, even for free tier!

1. Go to: https://platform.openai.com/account/billing
2. Click **"Add payment method"**
3. Add a credit card
4. Set a **usage limit** (e.g., $5/month) to avoid surprises

**Note**: The app uses GPT-4o by default. If you don't have access or want to save costs:
- Change `OPENAI_MODEL=gpt-4o` to `OPENAI_MODEL=gpt-3.5-turbo` in `.env`

---

## ✅ Step 3: Verify Setup

### Check Your Files

Make sure you have:

```
mindful-connect/
├── .env                        ← Updated with your API keys
├── serviceAccountKey.json      ← Downloaded from Firebase
└── venv/                       ← Virtual environment (already created)
```

### Your .env Should Look Like:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-YOUR_REAL_KEY_HERE  # ← Your actual key

# Firebase Configuration
FIREBASE_API_KEY=AIzaSyYOUR_REAL_KEY  # ← Your actual values
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abc123

# Firebase Admin SDK (Service Account)
FIREBASE_ADMIN_CREDENTIALS=./serviceAccountKey.json  # ← File must exist!

# Encryption (Already configured - don't change!)
AES_ENCRYPTION_KEY=WDrqj1JeQVobKZ5cGI4Oke2cNnvnW
SECRET_KEY=B4_9Qr8ZYuQQ81XLiWDrqj1JeQVobKZ5cGI4Oke2cNnvnW
```

---

## 🚀 Step 4: Run the App!

Once you've completed Steps 1-3, run:

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run the app
streamlit run src/app.py
```

The app will open at: **http://localhost:8501** 🎉

---

## 🎯 First Time Using the App

1. **Sign Up**: Create an account with email/password
2. **Log In**: Use your credentials
3. **Log Mood**: Click "📝 Log Mood" → Rate your mood → Add notes
4. **View Dashboard**: See AI insights and mood trends!

---

## 🐛 Troubleshooting

### "Firebase initialization failed"
- ✅ Check `serviceAccountKey.json` is in the project root
- ✅ Verify file path in `.env` is `./serviceAccountKey.json`
- ✅ Make sure all Firebase config values are correct

### "OpenAI API error"
- ✅ Verify your API key in `.env` is correct
- ✅ Check you have billing set up in OpenAI
- ✅ Try changing model to `gpt-3.5-turbo` if you don't have GPT-4 access

### "Module not found"
```powershell
.\venv\Scripts\activate
pip install -r requirements-core.txt
```

### "Port 8501 already in use"
```powershell
streamlit run src/app.py --server.port=8502
```

---

## 📋 Quick Checklist

Before running the app, make sure:

- [ ] Firebase project created
- [ ] Authentication enabled (Email/Password)
- [ ] Firestore database created
- [ ] `serviceAccountKey.json` downloaded and in project root
- [ ] Firebase config values added to `.env`
- [ ] OpenAI API key obtained
- [ ] OpenAI billing set up
- [ ] OpenAI API key added to `.env`
- [ ] Virtual environment activated

---

## 🎉 You're Ready!

Once all checkboxes are ✅, run:

```powershell
.\venv\Scripts\activate
streamlit run src/app.py
```

**Your AI-powered mental wellness app will be live!** 🚀

---

## 📞 Need Help?

- Check `QUICK_START.md` for more details
- Review `GETTING_STARTED.md` for comprehensive guide
- See `PROJECT_OVERVIEW.md` for features

---

**Current Status**: 
- ✅ Environment configured
- ✅ Encryption keys generated
- ⏳ Waiting for Firebase & OpenAI setup
