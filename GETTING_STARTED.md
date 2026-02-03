# 🚀 Getting Started with Mindful Connect

## Welcome! 👋

You now have a **complete, production-ready AI-powered mental wellness application**. This guide will help you get it running in the next 15-30 minutes.

## ⚡ Quick Start (5 Steps)

### Step 1: Set Up Firebase (10 minutes)

1. **Go to [Firebase Console](https://console.firebase.google.com/)**
   - Click "Add Project"
   - Name it "Mindful Connect" (or your choice)
   - Disable Google Analytics (optional)
   - Click "Create Project"

2. **Enable Authentication**
   - Click "Authentication" in left sidebar
   - Click "Get Started"
   - Click "Email/Password" → Enable → Save
   - (Optional) Enable "Google" provider

3. **Create Firestore Database**
   - Click "Firestore Database" in left sidebar
   - Click "Create Database"
   - Choose "Start in test mode"
   - Select your region (closest to you)
   - Click "Enable"

4. **Get Service Account Key**
   - Click gear icon → "Project Settings"
   - Go to "Service Accounts" tab
   - Click "Generate New Private Key"
   - Save the JSON file as `serviceAccountKey.json` in your project root

5. **Get Web App Config**
   - In "Project Settings" → "General" tab
   - Scroll to "Your apps"
   - Click the "</>" (web) icon
   - Register app with nickname "Mindful Connect Web"
   - Copy the config values (you'll need these for .env)

### Step 2: Get OpenAI API Key (5 minutes)

1. **Go to [OpenAI Platform](https://platform.openai.com/)**
   - Sign up or log in
   - Click your profile → "View API Keys"
   - Click "Create new secret key"
   - Name it "Mindful Connect"
   - **Copy the key immediately** (you won't see it again!)

### Step 3: Configure Environment (5 minutes)

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your values:**
   ```env
   # OpenAI (from Step 2)
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   
   # Firebase (from Step 1 - Web App Config)
   FIREBASE_API_KEY=AIzaSy...
   FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   FIREBASE_MESSAGING_SENDER_ID=123456789
   FIREBASE_APP_ID=1:123456789:web:abc123
   
   # Generate these keys (see below)
   AES_ENCRYPTION_KEY=your_32_character_key_here_12345
   SECRET_KEY=your_secret_key_minimum_32_characters_long_here
   ```

3. **Generate encryption keys** (run in Python):
   ```python
   import secrets
   print("AES Key:", secrets.token_urlsafe(32)[:32])
   print("Secret Key:", secrets.token_urlsafe(48))
   ```

### Step 4: Install and Initialize (5 minutes)

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   *Note: This may take 5-10 minutes as it downloads AI models*

4. **Initialize database:**
   ```bash
   python scripts/init_database.py
   ```

### Step 5: Run the App! (1 minute)

```bash
streamlit run src/app.py
```

**That's it!** Your app should open at `http://localhost:8501` 🎉

## 🎯 First Time Using the App

1. **Sign Up**
   - Click "Sign Up" tab
   - Enter email and password
   - Click "Sign Up"
   - Check your email for verification (optional)

2. **Log In**
   - Enter your credentials
   - Click "Login"

3. **Log Your First Mood**
   - Click "📝 Log Mood" in sidebar
   - Move the slider to rate your mood
   - (Optional) Select triggers
   - (Optional) Write a journal entry
   - Click "Save Mood Entry"
   - Wait for AI-generated insights!

4. **View Dashboard**
   - Click "📊 Dashboard" in sidebar
   - See your mood trends
   - View AI insights
   - Check mood predictions

## 🧪 Testing the Application

Run the test suite to verify everything works:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src --cov-report=html

# View coverage (open in browser)
# htmlcov/index.html
```

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### "Firebase initialization failed"
- Check that `serviceAccountKey.json` is in the project root
- Verify the file path in `.env` is correct
- Ensure Firebase project ID matches

### "OpenAI API error"
- Verify your API key is correct in `.env`
- Check you have credits/billing set up
- Ensure you have GPT-4o access (or change model to gpt-3.5-turbo)

### "Port 8501 already in use"
```bash
# Use a different port
streamlit run src/app.py --server.port=8502
```

### "Import errors with transformers"
```bash
# The first run downloads AI models (this is normal)
# Wait for the download to complete
# If it fails, try:
pip install --upgrade transformers torch
```

## 📚 What's Next?

### Explore the Features
- ✅ Log multiple mood entries
- ✅ View mood trends over time
- ✅ Get AI-generated insights
- ✅ See mood predictions
- ✅ Track patterns and triggers

### Customize the App
- Edit `src/app.py` to change UI
- Modify AI prompts in `src/ai/openai_client.py`
- Adjust mood prediction in `src/ai/mood_predictor.py`
- Update styling in the CSS section

### Deploy to Production
- See `SETUP_GUIDE.md` for Heroku deployment
- See `SETUP_GUIDE.md` for Vercel deployment
- Use Docker for containerized deployment

### Add Advanced Features
- Implement wearable integration (Fitbit/Apple Health)
- Complete AI chat therapy module
- Set up push notifications
- Add social features

## 📖 Documentation

- **README.md**: Full project documentation
- **SETUP_GUIDE.md**: Detailed setup instructions
- **PROJECT_OVERVIEW.md**: Feature list and architecture
- **Code Comments**: Inline documentation in all files

## 🆘 Getting Help

1. **Check the logs**: `logs/mindful_connect.log`
2. **Review documentation**: Start with `SETUP_GUIDE.md`
3. **Test individual components**: Use pytest to isolate issues
4. **Check Firebase Console**: Verify authentication and database
5. **Verify API keys**: Ensure all keys in `.env` are correct

## 💡 Pro Tips

1. **Start with test mode**: Use Firebase test mode initially
2. **Monitor API usage**: Check OpenAI usage dashboard
3. **Use version control**: Commit your changes regularly
4. **Test locally first**: Before deploying to production
5. **Enable Sentry**: Set up error tracking for production

## 🎉 Success Checklist

- [ ] Firebase project created
- [ ] OpenAI API key obtained
- [ ] `.env` file configured
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] App running on localhost
- [ ] Successfully signed up
- [ ] First mood entry logged
- [ ] AI insights received
- [ ] Dashboard displaying data

## 🚀 You're Ready!

Once you've completed the checklist above, you have a **fully functional AI-powered mental wellness application**!

### What You've Built:
- ✅ Secure user authentication
- ✅ Encrypted data storage
- ✅ AI-powered mood analysis
- ✅ Predictive mood forecasting
- ✅ Beautiful, modern UI
- ✅ Production-ready architecture

**Congratulations on building an amazing mental wellness tool!** 🎊

---

*Need help? Check SETUP_GUIDE.md or open an issue on GitHub*

**Happy coding! 💙**
