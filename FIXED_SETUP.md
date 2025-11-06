# 🔧 FIXED AutoQuery Setup for Windows 11

## ✅ What I Fixed

1. **Made FAISS optional** - App works without it
2. **Better error handling** - Won't crash if packages missing
3. **Simpler requirements** - Only essentials needed
4. **Test scripts** - Verify installation easily
5. **Minimal test server** - Test basic functionality first

---

## 🚀 Easy Setup (Step-by-Step)

### Step 1: Install Prerequisites

**Python 3.10+:**
1. Download: https://www.python.org/downloads/
2. ⚠️ **CRITICAL:** Check "Add Python to PATH" during installation
3. Click "Install Now"
4. Test: Open Command Prompt and type `python --version`

**Node.js 18+:**
1. Download: https://nodejs.org/ (LTS version)
2. Install with default settings
3. Test: `node --version`

---

### Step 2: Backend Setup (Minimal Install)

Open **Command Prompt** (Win + R, type `cmd`, press Enter)

```cmd
REM Navigate to project
cd path\to\autoquery\backend

REM Create virtual environment
python -m venv venv

REM Activate it
venv\Scripts\activate

REM You should see (venv) at the start of your line now

REM Upgrade pip
python -m pip install --upgrade pip

REM Install ONLY essential packages
pip install fastapi==0.109.0
pip install uvicorn==0.27.0
pip install openai==1.12.0
pip install python-dotenv==1.0.1
pip install PyPDF2==3.0.1
pip install python-docx==1.1.0
pip install pydantic==2.6.1

REM Create .env file
copy .env.example .env

REM Edit it (this opens Notepad)
notepad .env
```

**In Notepad:**
- Find: `OPENAI_API_KEY=sk-your-openai-api-key-here`
- Replace with your actual API key from https://platform.openai.com/api-keys
- Save and close

---

### Step 3: Test Your Installation

```cmd
REM Still in backend folder with venv activated
python test_installation.py
```

**This will check:**
- ✅ Python version
- ✅ All required packages
- ✅ OpenAI API key
- ✅ Configuration

**If you see errors, follow the instructions it gives you!**

---

### Step 4: Test Basic Server

```cmd
REM Test with minimal server first
python main_test.py
```

**Expected output:**
```
Starting AutoQuery Test Server
✅ Server will start on: http://localhost:8000
✅ OpenAI client initialized successfully!
```

**Open browser:** http://localhost:8000

You should see: `"AutoQuery Test Server is running! 🚀"`

**If this works, great! Press Ctrl+C and continue.**

---

### Step 5: Start Full Backend

```cmd
REM In same terminal
python main.py
```

**Expected:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is running!** Keep this window open.

---

### Step 6: Frontend Setup

Open a **NEW Command Prompt** (keep backend running!)

```cmd
cd path\to\autoquery\frontend

REM Install packages (this takes 2-3 minutes)
npm install

REM If the above fails, try:
npm install --legacy-peer-deps

REM Copy environment file
copy .env.example .env

REM Start frontend
npm run dev
```

**Expected:**
```
VITE v5.0.8  ready in 500 ms
➜  Local:   http://localhost:5173/
```

✅ **Frontend is running!**

---

### Step 7: Test the App

1. **Open browser:** http://localhost:5173
2. **You should see AutoQuery!** 🎉
3. **Type a message:** "Hello! Introduce yourself"
4. **Press Enter**
5. **You should get AI response!**

---

## 🎯 If You Want Document Upload (Optional)

The basic version works for chat. To enable document upload with smart search:

```cmd
cd backend
venv\Scripts\activate

REM Install additional packages
pip install langchain==0.1.9
pip install tiktoken==0.6.0

REM Try to install FAISS (may fail on Windows)
pip install faiss-cpu --no-cache-dir

REM If FAISS fails, that's OK!
REM Document upload will still work, just with simpler search
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "python is not recognized"
**Solution:**
- Reinstall Python
- **MUST** check "Add Python to PATH"
- Restart Command Prompt

### Issue 2: "cannot activate venv"
**PowerShell solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try: `venv\Scripts\Activate.ps1`

### Issue 3: pip install fails
**Solution:**
```cmd
REM Install one by one
pip install fastapi
pip install uvicorn
pip install openai
REM etc...
```

### Issue 4: "OpenAI API error"
**Check:**
- Open `backend\.env` in Notepad
- Format should be: `OPENAI_API_KEY=sk-proj-xxxxx`
- No spaces around `=`
- No quotes
- Key starts with `sk-`

### Issue 5: Frontend npm install fails
**Solution:**
```cmd
npm cache clean --force
npm install --legacy-peer-deps
```

### Issue 6: "Port 8000 already in use"
**Solution:**
```cmd
netstat -ano | findstr :8000
REM Note the PID number
taskkill /PID <number> /F
```

---

## 📋 Quick Command Reference

### Start Backend:
```cmd
cd backend
venv\Scripts\activate
python main.py
```

### Start Frontend (NEW terminal):
```cmd
cd frontend
npm run dev
```

### Test Installation:
```cmd
cd backend
venv\Scripts\activate
python test_installation.py
```

### Test Minimal Server:
```cmd
cd backend
venv\Scripts\activate
python main_test.py
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] `python --version` shows 3.10+
- [ ] `node --version` shows 18+
- [ ] `test_installation.py` passes all core tests
- [ ] `main_test.py` starts without errors
- [ ] Can access http://localhost:8000
- [ ] `main.py` starts without errors
- [ ] `npm run dev` starts without errors
- [ ] Can access http://localhost:5173
- [ ] Can send chat messages
- [ ] AI responds correctly

---

## 🎯 Success!

If you can:
1. ✅ Start both servers
2. ✅ Open http://localhost:5173
3. ✅ Send a message
4. ✅ Get AI response

**Congratulations! It's working!** 🎉

Now you can:
- Try uploading documents
- Ask questions about them
- Add this to your resume!

---

## 💡 Pro Tips

1. **Always activate venv first** before running Python commands
2. **Keep both terminals open** - need backend AND frontend
3. **Use test_installation.py** to verify your setup
4. **Start with main_test.py** if having issues
5. **FAISS is optional** - don't worry if it won't install

---

## 📞 Still Having Problems?

### Try This Order:

1. **Run test_installation.py** - see what's missing
2. **Try main_test.py** - test basic functionality
3. **Check .env file** - make sure API key is correct
4. **Restart Command Prompt** - fresh start
5. **Try minimal requirements** - fewer packages

### Files to Help:
- `test_installation.py` - Diagnose problems
- `main_test.py` - Test basic setup
- `requirements-minimal.txt` - Minimal packages
- `WINDOWS_INSTALL.md` - Detailed guide
- `WINDOWS_SETUP.md` - Troubleshooting

---

**The code is now fixed and should work on Windows 11! 🚀**

**Good luck!** 🎉
