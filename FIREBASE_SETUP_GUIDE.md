# Firebase Setup - Step-by-Step Visual Guide

## PART 1: Create Firebase Project

### Step 1: Go to Firebase Console
1. Open your browser
2. Go to: **https://console.firebase.google.com/**
3. Sign in with your Google account

### Step 2: Create New Project
1. Click the **"Add project"** or **"Create a project"** button
2. You'll see a wizard with 3 steps:

**Screen 1 - Project Name:**
- Enter project name: `mindful-connect` (or any name you prefer)
- Click **"Continue"**

**Screen 2 - Google Analytics:**
- Toggle OFF "Enable Google Analytics" (not needed for now)
- Click **"Create project"**

**Screen 3 - Wait:**
- Wait 30-60 seconds for project creation
- Click **"Continue"** when ready

---

## PART 2: Enable Authentication

### Step 3: Set Up Authentication
1. In the left sidebar, click **"Build"** to expand it
2. Click **"Authentication"**
3. Click the **"Get started"** button
4. You'll see "Sign-in method" tab

### Step 4: Enable Email/Password
1. Click on **"Email/Password"** in the providers list
2. Toggle **ON** the first switch (Email/Password)
3. Leave the second switch (Email link) OFF
4. Click **"Save"**

You should see "Email/Password" now shows as "Enabled"

---

## PART 3: Create Firestore Database

### Step 5: Set Up Firestore
1. In the left sidebar, click **"Firestore Database"**
2. Click **"Create database"** button

### Step 6: Configure Database
**Screen 1 - Security Rules:**
- Select **"Start in test mode"**
  (This allows read/write access for 30 days - we'll secure it later)
- Click **"Next"**

**Screen 2 - Location:**
- Choose the region closest to you
  - US: `us-central1` or `us-east1`
  - Europe: `europe-west1`
  - Asia: `asia-south1` or `asia-southeast1`
- Click **"Enable"**
- Wait 1-2 minutes for database creation

---

## PART 4: Get Service Account Key (CRITICAL!)

### Step 7: Download Service Account Key
1. Click the **gear icon** (⚙️) next to "Project Overview" in the left sidebar
2. Click **"Project settings"**
3. Go to the **"Service accounts"** tab
4. You'll see "Firebase Admin SDK" section
5. Click **"Generate new private key"** button
6. A popup appears - Click **"Generate key"**
7. A JSON file will download to your computer

### Step 8: Move the File
1. Find the downloaded file (usually in Downloads folder)
   - It's named something like: `mindful-connect-abc123-firebase-adminsdk-xyz.json`
2. **RENAME** it to exactly: `serviceAccountKey.json`
3. **MOVE** it to your project folder:
   ```
   C:\Users\akhil\.gemini\antigravity\scratch\mindful-connect\serviceAccountKey.json
   ```

**IMPORTANT:** The file MUST be in the root of your project folder!

---

## PART 5: Get Web App Configuration

### Step 9: Register Web App
1. Still in **"Project settings"** → Go to **"General"** tab
2. Scroll down to **"Your apps"** section
3. Click the **"</>"** icon (Web platform)
4. A popup appears:
   - **App nickname:** `Mindful Connect Web`
   - **DO NOT** check "Also set up Firebase Hosting"
   - Click **"Register app"**

### Step 10: Copy Configuration
You'll see code that looks like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyABC123...",
  authDomain: "mindful-connect-abc123.firebaseapp.com",
  projectId: "mindful-connect-abc123",
  storageBucket: "mindful-connect-abc123.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abc123def456",
  measurementId: "G-ABC123XYZ"
};
```

**COPY THESE VALUES!** You'll need them in the next step.

Click **"Continue to console"** when done.

---

## PART 6: Update .env File

### Step 11: Configure Environment Variables

1. Open your `.env` file in the project
2. Find these lines and UPDATE them with YOUR values:

```env
# Firebase Configuration
FIREBASE_API_KEY=AIzaSyABC123...              # ← Paste YOUR apiKey
FIREBASE_AUTH_DOMAIN=mindful-connect-abc123.firebaseapp.com  # ← YOUR authDomain
FIREBASE_PROJECT_ID=mindful-connect-abc123    # ← YOUR projectId
FIREBASE_STORAGE_BUCKET=mindful-connect-abc123.appspot.com   # ← YOUR storageBucket
FIREBASE_MESSAGING_SENDER_ID=123456789012     # ← YOUR messagingSenderId
FIREBASE_APP_ID=1:123456789012:web:abc123def456  # ← YOUR appId
FIREBASE_MEASUREMENT_ID=G-ABC123XYZ           # ← YOUR measurementId (optional)
```

3. **SAVE** the `.env` file

---

## VERIFICATION CHECKLIST

Before proceeding, verify you have:

- [ ] Firebase project created
- [ ] Authentication enabled (Email/Password)
- [ ] Firestore database created (in test mode)
- [ ] `serviceAccountKey.json` downloaded
- [ ] `serviceAccountKey.json` renamed correctly
- [ ] `serviceAccountKey.json` moved to project root folder
- [ ] `.env` file updated with all Firebase config values
- [ ] `.env` file saved

---

## NEXT STEP

Once you've completed all the above:

1. Run the test script to verify:
   ```powershell
   .\venv\Scripts\activate
   python test_setup.py
   ```

2. If Firebase checks pass, you're ready for OpenAI setup!

---

## TROUBLESHOOTING

### "I can't find the downloaded JSON file"
- Check your Downloads folder
- Look for a file with "firebase-adminsdk" in the name
- Make sure you clicked "Generate key" not just viewed the page

### "The .env file won't save"
- Make sure you're editing the file in the project root
- Don't edit `.env.example` - edit `.env`
- Save with Ctrl+S

### "I don't see the gear icon"
- Look in the top-left corner, next to "Project Overview"
- It's a small gear/cog icon
- Click it, then "Project settings"

---

## VISUAL REFERENCE

Your project folder should look like this:

```
mindful-connect/
├── .env                        ← Updated with Firebase config
├── serviceAccountKey.json      ← Downloaded from Firebase ✓
├── src/
├── venv/
└── ...
```

---

**Once you complete this, Firebase setup is DONE!** ✓

Next: OpenAI API setup (5 minutes)
