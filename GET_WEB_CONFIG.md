# Get Firebase Web Config - Quick Instructions

Your Firebase project: mindful-connect-97471

## Get Your Web App Configuration:

1. Go to: https://console.firebase.google.com/project/mindful-connect-97471/settings/general

2. Scroll down to "Your apps" section

3. Look for a web app (</> icon)
   - If you see one, click on it
   - If you don't see one, click the "</>" icon to create a web app

4. You'll see code like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "mindful-connect-97471.firebaseapp.com",
  projectId: "mindful-connect-97471",
  storageBucket: "mindful-connect-97471.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

5. Copy ALL these values and paste them here

## OR Use These Likely Values:

Based on your project ID, your config is likely:

```
FIREBASE_API_KEY=<YOU NEED TO GET THIS>
FIREBASE_AUTH_DOMAIN=mindful-connect-97471.firebaseapp.com
FIREBASE_PROJECT_ID=mindful-connect-97471
FIREBASE_STORAGE_BUCKET=mindful-connect-97471.appspot.com
FIREBASE_MESSAGING_SENDER_ID=<YOU NEED TO GET THIS>
FIREBASE_APP_ID=<YOU NEED TO GET THIS>
```

Please paste your complete firebaseConfig here!
