# 🚀 Complete Setup Guide for Beginners

This guide will help you set up AutoQuery **from scratch**, even if you're new to web development!

---

## 📚 Table of Contents

1. [Prerequisites Installation](#1-prerequisites-installation)
2. [Getting OpenAI API Key](#2-getting-openai-api-key)
3. [Backend Setup](#3-backend-setup)
4. [Frontend Setup](#4-frontend-setup)
5. [Testing the Application](#5-testing-the-application)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Prerequisites Installation

### For Windows Users:

#### Install Python 3.10+
1. Go to https://www.python.org/downloads/
2. Download Python 3.10 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   ```

#### Install Node.js 18+
1. Go to https://nodejs.org/
2. Download the LTS version
3. Run the installer
4. Verify installation:
   ```cmd
   node --version
   npm --version
   ```

### For macOS Users:

#### Install Python
```bash
# Using Homebrew (recommended)
brew install python@3.10
```

#### Install Node.js
```bash
# Using Homebrew
brew install node
```

### For Linux Users:

#### Install Python
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv
```

#### Install Node.js
```bash
# Using NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## 2. Getting OpenAI API Key

### Step-by-Step:

1. **Create an OpenAI Account**
   - Go to https://platform.openai.com/signup
   - Sign up with your email

2. **Verify Your Account**
   - Check your email and verify your account

3. **Add Payment Method** (Optional but recommended)
   - Go to https://platform.openai.com/account/billing
   - Add a payment method
   - **Note**: You get $5 free credits!

4. **Create API Key**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - **IMPORTANT**: Copy the key immediately (you won't see it again!)
   - Save it in a safe place

5. **Example API Key format:**
   ```
   sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 3. Backend Setup

### Step 1: Navigate to Backend

```bash
cd autoquery/backend
```

### Step 2: Create Virtual Environment

**Why?** To keep Python packages isolated from other projects.

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal now!

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take 2-5 minutes. Don't worry if you see some warnings!

### Step 4: Configure Environment Variables

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file:**
   
   **Windows:** Open with Notepad
   ```cmd
   notepad .env
   ```

   **macOS/Linux:** Open with nano
   ```bash
   nano .env
   ```

3. **Add your OpenAI API key:**
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```

4. **Save and close:**
   - Notepad: File → Save
   - nano: Ctrl+X → Y → Enter

### Step 5: Run the Backend

```bash
python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is now running!** Keep this terminal open.

### Step 6: Test Backend (Optional)

Open a new terminal and test:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Or open in browser:
# http://localhost:8000/docs  (API Documentation)
```

---

## 4. Frontend Setup

**Open a NEW terminal** (keep backend running!)

### Step 1: Navigate to Frontend

```bash
cd autoquery/frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This will take 2-5 minutes. Don't worry about warnings!

### Step 3: Configure Environment Variables

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. The default should work:
   ```
   VITE_API_URL=http://localhost:8000
   ```

### Step 4: Run the Frontend

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ **Frontend is now running!**

---

## 5. Testing the Application

### Step 1: Open in Browser

Go to: http://localhost:5173

You should see the AutoQuery interface!

### Step 2: Test Chat (Without Documents)

1. Type: "Hello, can you introduce yourself?"
2. Press Enter
3. You should get a response from the AI!

### Step 3: Test Document Upload

1. **Create a test document:**
   - Create a text file named `test.txt`
   - Write some content in it

2. **Upload it:**
   - Click the paperclip icon 📎
   - Select `test.txt`
   - Wait for upload confirmation

3. **Ask a question:**
   - Type: "What is in the uploaded document?"
   - Press Enter
   - AI should answer based on your document!

---

## 6. Troubleshooting

### Problem: "Python not found"

**Solution:**
```bash
# Try with python3 instead of python
python3 --version
python3 -m venv venv
```

### Problem: "pip: command not found"

**Solution:**
```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

### Problem: "npm: command not found"

**Solution:**
- Reinstall Node.js
- Make sure to restart your terminal after installation

### Problem: "OpenAI API Error: Invalid API Key"

**Solution:**
1. Check your `.env` file in the backend folder
2. Make sure there are no spaces around the `=` sign
3. Make sure the key starts with `sk-`
4. Try regenerating the key from OpenAI

### Problem: "CORS Error in Browser Console"

**Solution:**
1. Make sure backend is running on port 8000
2. Make sure frontend `.env` has: `VITE_API_URL=http://localhost:8000`
3. Restart both servers

### Problem: "Port 8000 already in use"

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Problem: "Module 'faiss' not found"

**Solution:**
```bash
pip uninstall faiss faiss-cpu
pip install faiss-cpu --no-cache-dir
```

### Problem: "Cannot upload files"

**Solution:**
1. Check backend terminal for errors
2. Make sure `uploads` folder exists in backend directory
3. Check file size (max 10MB)
4. Check file format (only PDF, DOCX, TXT)

---

## 🎯 Quick Reference Commands

### Backend:
```bash
cd autoquery/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

### Frontend:
```bash
cd autoquery/frontend
npm run dev
```

### Stop Servers:
- Press `Ctrl+C` in each terminal

---

## 📝 Next Steps

Once everything is working:

1. ✅ Try uploading different document types
2. ✅ Ask complex questions
3. ✅ Test error handling
4. ✅ Read the code and understand how it works
5. ✅ Customize the UI
6. ✅ Add it to your resume!

---

## 🆘 Still Having Issues?

### Check These:

1. **Both servers running?**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:5173

2. **Environment variables set?**
   - Backend: `.env` with OpenAI API key
   - Frontend: `.env` with API URL

3. **Dependencies installed?**
   - Backend: `pip list` shows all packages
   - Frontend: `node_modules` folder exists

4. **Firewalls/Antivirus?**
   - Sometimes they block local servers
   - Try disabling temporarily

### Get Help:

1. Check the error message carefully
2. Search the error on Google
3. Check FastAPI logs in backend terminal
4. Check browser console (F12) for frontend errors

---

## ✅ Success Checklist

Before you say "it's working!":

- [ ] Backend starts without errors
- [ ] Frontend opens in browser
- [ ] Can send chat messages
- [ ] Can upload documents
- [ ] AI responds to questions
- [ ] Documents appear in sidebar
- [ ] Can ask questions about documents

---

**Congratulations! 🎉 You've successfully set up AutoQuery!**

Now you can:
- Add it to your resume
- Show it in interviews
- Learn from the code
- Build something even better!

Happy coding! 🚀
