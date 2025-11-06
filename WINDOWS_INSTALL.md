# 🪟 Windows 11 - Step by Step Installation

## 📋 Before You Start

Make sure you have:
- ✅ Windows 11
- ✅ Python 3.10+ installed
- ✅ Node.js 18+ installed
- ✅ OpenAI API key ready

---

## 🎯 Method 1: Easiest Setup (Recommended for Windows)

### Step 1: Extract the Project

1. Extract `autoquery.zip` to your desktop
2. You should have a folder: `C:\Users\YourName\Desktop\autoquery`

### Step 2: Backend Setup (Python)

**Open Command Prompt:**
- Press `Win + R`
- Type `cmd`
- Press Enter

**Run these commands one by one:**

```cmd
cd C:\Users\YourName\Desktop\autoquery\backend

python -m venv venv

venv\Scripts\activate

python -m pip install --upgrade pip

pip install fastapi==0.109.0

pip install uvicorn==0.27.0

pip install openai==1.12.0

pip install python-dotenv==1.0.1

pip install PyPDF2==3.0.1

pip install python-docx==1.1.0

pip install pydantic==2.6.1

copy .env.example .env

notepad .env
```

**In Notepad:**
- Replace `sk-your-openai-api-key-here` with your actual API key
- Save and close

### Step 3: Test Backend

**Still in the same Command Prompt:**

```cmd
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Success!** Backend is running. **Keep this window open!**

### Step 4: Frontend Setup (React)

**Open a NEW Command Prompt** (keep the first one running):
- Press `Win + R`
- Type `cmd`
- Press Enter

**Run these commands:**

```cmd
cd C:\Users\YourName\Desktop\autoquery\frontend

npm install

npm run dev
```

**Expected output:**
```
VITE v5.0.8  ready in 500 ms
➜  Local:   http://localhost:5173/
```

✅ **Success!** Frontend is running.

### Step 5: Open in Browser

1. Open Chrome/Edge
2. Go to: `http://localhost:5173`
3. You should see AutoQuery! 🎉

---

## 🎯 Method 2: Using the Setup Script

1. Extract autoquery.zip
2. Double-click `setup-windows.bat`
3. Follow the on-screen instructions

---

## ⚠️ Common Errors & Quick Fixes

### Error: "python is not recognized"

**Fix:**
1. Download Python: https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH"
3. Install
4. Close and reopen Command Prompt
5. Test: `python --version`

### Error: "node is not recognized"

**Fix:**
1. Download Node.js: https://nodejs.org/
2. Install the LTS version
3. Close and reopen Command Prompt
4. Test: `node --version`

### Error: "pip install" fails

**Try this:**
```cmd
pip install <package-name> --user
```

### Error: "Cannot activate venv"

**If using PowerShell, run:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Error: "Port 8000 is already in use"

**Fix:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <number> /F
```

Replace `<number>` with the PID shown.

### Error: npm install fails

**Try:**
```cmd
npm cache clean --force
npm install --legacy-peer-deps
```

---

## 🧪 Testing the Application

### Test 1: Basic Chat (No Documents)

1. Open http://localhost:5173
2. Type: "Hello! Introduce yourself"
3. Press Enter
4. You should get a response from AI

### Test 2: Document Upload

1. Create a text file: `test.txt`
2. Write something in it: "This is a test document about cats."
3. Click the paperclip icon 📎
4. Upload `test.txt`
5. Wait for "Document uploaded" message
6. Ask: "What is in the document?"
7. AI should tell you about cats!

---

## 📝 What If FAISS Won't Install?

FAISS is for document search and can be tricky on Windows.

**Option 1: Skip it for now**
- The app will work for basic chat without FAISS
- You can add it later

**Option 2: Install separately**
```cmd
pip install faiss-cpu --no-cache-dir
```

**Option 3: Use minimal version**
```cmd
cd backend
pip install -r requirements-minimal.txt
```

---

## 🎯 Quick Reference

### Start Backend:
```cmd
cd autoquery\backend
venv\Scripts\activate
python main.py
```

### Start Frontend:
```cmd
cd autoquery\frontend
npm run dev
```

### Stop Servers:
Press `Ctrl + C` in each terminal

---

## ✅ Success Checklist

- [ ] Python installed and in PATH
- [ ] Node.js installed and in PATH
- [ ] OpenAI API key added to backend\.env
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can open http://localhost:5173
- [ ] Can send chat messages
- [ ] Can upload documents (if FAISS installed)

---

## 💡 Pro Tips

1. **Keep both terminals open** - You need backend AND frontend running

2. **Use Windows Terminal** - Better than cmd
   - Install from Microsoft Store

3. **Check firewall** - May block local servers
   - Allow Python and Node.js

4. **Restart if needed** - Sometimes Windows needs a restart after installing Python/Node

---

## 📞 Still Not Working?

### Check These:

1. **Python version:**
   ```cmd
   python --version
   ```
   Should be 3.10 or higher

2. **Node version:**
   ```cmd
   node --version
   ```
   Should be 18 or higher

3. **OpenAI key:**
   - Check backend\.env file
   - Format: `OPENAI_API_KEY=sk-...`
   - No spaces, no quotes

4. **Firewall/Antivirus:**
   - May block installations
   - Try disabling temporarily

---

## 🎉 It's Working!

Great! Now you can:
1. Upload documents (PDF, DOCX, TXT)
2. Ask questions about them
3. Get AI-powered answers
4. Show it off in your resume! 🚀

---

**Need more help?** Check `WINDOWS_SETUP.md` for detailed troubleshooting!
