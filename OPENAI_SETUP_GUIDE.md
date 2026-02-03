# OpenAI API Setup - Step-by-Step Guide

## PART 1: Create OpenAI Account & Get API Key

### Step 1: Go to OpenAI Platform
1. Open your browser
2. Go to: **https://platform.openai.com/**
3. Click **"Sign up"** or **"Log in"**

### Step 2: Create Account (if new)
- Sign up with Google, Microsoft, or email
- Verify your email if required
- Complete the signup process

### Step 3: Navigate to API Keys
1. Once logged in, click your **profile icon** (top-right corner)
2. Click **"View API keys"** or **"API keys"**
3. Or go directly to: https://platform.openai.com/api-keys

### Step 4: Create New API Key
1. Click the **"+ Create new secret key"** button
2. A dialog appears:
   - **Name:** `Mindful Connect` (or any name)
   - **Permissions:** Leave as default (All)
   - Click **"Create secret key"**

### Step 5: Copy Your API Key
1. **CRITICAL:** Copy the key IMMEDIATELY!
   - It looks like: `sk-proj-abc123...`
   - You will NEVER see it again!
2. Click **"Copy"** button
3. Paste it somewhere safe temporarily (Notepad)
4. Click **"Done"**

---

## PART 2: Set Up Billing (REQUIRED!)

**IMPORTANT:** OpenAI requires a payment method, even for the free tier!

### Step 6: Add Payment Method
1. Click **"Settings"** in the left sidebar
2. Click **"Billing"** tab
3. Or go to: https://platform.openai.com/account/billing/overview

### Step 7: Add Credit Card
1. Click **"Add payment method"**
2. Enter your credit card details
3. Click **"Save"**

### Step 8: Set Usage Limits (Recommended)
1. Go to **"Limits"** tab in Billing
2. Set a **monthly budget limit**:
   - For testing: $5/month is plenty
   - For production: $20-50/month
3. This prevents unexpected charges!

---

## PART 3: Configure Your App

### Step 9: Update .env File
1. Open your `.env` file in the project
2. Find this line:
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
3. Replace with YOUR actual key:
   ```env
   OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
   ```
4. **SAVE** the file

---

## OPTIONAL: Choose Your Model

### Default Model: GPT-4o (Recommended)
Your `.env` is already set to use `gpt-4o`:
```env
OPENAI_MODEL=gpt-4o
```

**Pros:**
- Best quality responses
- Most intelligent insights
- Better understanding

**Cons:**
- More expensive (~$0.01 per request)
- Requires GPT-4 access

### Alternative: GPT-3.5 Turbo (Cheaper)
If you want to save money or don't have GPT-4 access:

Change in `.env`:
```env
OPENAI_MODEL=gpt-3.5-turbo
```

**Pros:**
- Much cheaper (~$0.001 per request)
- Faster responses
- Available to everyone

**Cons:**
- Lower quality insights
- Less nuanced understanding

---

## VERIFICATION CHECKLIST

Before proceeding, verify you have:

- [ ] OpenAI account created
- [ ] API key generated
- [ ] API key copied (starts with `sk-proj-` or `sk-`)
- [ ] Payment method added to OpenAI account
- [ ] Usage limit set (optional but recommended)
- [ ] `.env` file updated with API key
- [ ] `.env` file saved

---

## TEST YOUR SETUP

Run the verification script:

```powershell
.\venv\Scripts\activate
python test_setup.py
```

If all checks pass, you're ready to run the app!

---

## COST ESTIMATES

### Typical Usage for Testing (1 week):
- 50 mood entries with AI insights
- **GPT-4o:** ~$0.50
- **GPT-3.5-turbo:** ~$0.05

### Typical Usage for Production (1 month, 100 users):
- 3,000 mood entries
- **GPT-4o:** ~$30
- **GPT-3.5-turbo:** ~$3

**Recommendation:** Start with GPT-3.5-turbo for testing, upgrade to GPT-4o for production.

---

## TROUBLESHOOTING

### "I don't see the API keys page"
- Make sure you're logged in
- Go directly to: https://platform.openai.com/api-keys
- Check you're on the Platform site, not the ChatGPT site

### "Create new secret key button is disabled"
- You need to add a payment method first
- Go to Billing → Add payment method

### "My API key doesn't work"
- Make sure you copied the ENTIRE key (starts with `sk-`)
- Check for extra spaces in the `.env` file
- Verify the key in OpenAI dashboard is active

### "I'm getting billing errors"
- Check you have a valid payment method
- Verify your card hasn't expired
- Check you haven't exceeded your usage limit

### "I want to use GPT-4 but don't have access"
- GPT-4 access is automatic with a paid account
- Make sure you've added a payment method
- If still no access, use `gpt-3.5-turbo` instead

---

## SECURITY BEST PRACTICES

1. **Never commit your API key to Git**
   - The `.env` file is already in `.gitignore`
   - Never share your key publicly

2. **Rotate keys regularly**
   - Create new keys every few months
   - Delete old keys you're not using

3. **Monitor usage**
   - Check your OpenAI dashboard regularly
   - Set up usage alerts

4. **Use environment variables**
   - Never hardcode keys in your code
   - Always use `.env` file

---

## NEXT STEPS

Once OpenAI is configured:

1. ✓ Firebase setup complete
2. ✓ OpenAI setup complete
3. Run: `python test_setup.py`
4. Run: `streamlit run src/app.py`
5. Create your first account!
6. Log your first mood!
7. See AI-powered insights! 🎉

---

**Your API key is the final piece! Once configured, you're ready to launch!** 🚀
