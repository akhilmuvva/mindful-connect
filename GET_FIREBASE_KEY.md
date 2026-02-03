# Get Firebase Service Account Key - Quick Guide

## You Need: serviceAccountKey.json

This file is CRITICAL for your app to work with Firebase.

### How to Get It:

1. **Go to Firebase Console**
   - Open: https://console.firebase.google.com/
   - Select your existing Firebase project

2. **Open Project Settings**
   - Click the gear icon (⚙️) next to "Project Overview"
   - Click "Project settings"

3. **Go to Service Accounts Tab**
   - Click the "Service accounts" tab at the top

4. **Generate New Private Key**
   - Scroll down to "Firebase Admin SDK" section
   - Click "Generate new private key" button
   - Click "Generate key" in the popup
   - A JSON file will download

5. **Rename and Move the File**
   - Find the downloaded file in your Downloads folder
   - Rename it to exactly: serviceAccountKey.json
   - Move it to: C:\Users\akhil\.gemini\antigravity\scratch\mindful-connect\

### Verify:
The file should be at:
C:\Users\akhil\.gemini\antigravity\scratch\mindful-connect\serviceAccountKey.json

---

## Next: Update Firebase Config in .env

After you have the serviceAccountKey.json, we'll update your .env file with your Firebase project details.
