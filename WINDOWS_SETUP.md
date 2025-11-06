# 🪟 Windows 11 Setup & Troubleshooting Guide

## 🚀 Quick Setup for Windows 11

### Method 1: Automatic Setup (Recommended)

1. **Open Command Prompt or PowerShell**
   - Press `Win + R`
   - Type `cmd` and press Enter

2. **Navigate to the project folder**
   ```cmd
   cd path\to\autoquery
   ```

3. **Run the setup script**
   ```cmd
   setup-windows.bat
   ```

That's it! The script will install everything automatically.

---

### Method 2: Manual Setup

If the automatic setup fails, follow these steps:

#### Backend Setup:

```cmd
cd backend

REM Create virtual environment
python -m venv venv

REM Activate it
venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install packages ONE BY ONE (if batch install fails)
pip install fastapi==0.109.0
pip install uvicorn[standard]==0.27.0
pip install openai==1.12.0
pip install langchain==0.1.9
pip install python-dotenv==1.0.1
pip install PyPDF2==3.0.1
pip install python-docx==1.1.0
pip install pydantic==2.6.1
pip install pydantic-settings==2.1.0

REM Install FAISS (important!)
pip install faiss-cpu --no-cache-dir

REM Copy environment file
copy .env.example .env

REM Edit .env and add your OpenAI API key
notepad .env
```

#### Frontend Setup:

```cmd
cd frontend

REM Install npm packages
npm install

REM If above fails, try:
npm install --legacy-peer-deps

REM Copy environment file
copy .env.example .env
```

---

## ⚠️ Common Windows 11 Issues & Solutions

### Issue 1: "python is not recognized"

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Restart Command Prompt
4. Test: `python --version`

### Issue 2: "node is not recognized"

**Solution:**
1. Download Node.js from https://nodejs.org/
2. Install the LTS version
3. Restart Command Prompt
4. Test: `node --version`

### Issue 3: "Microsoft Visual C++ 14.0 is required"

This happens when installing some Python packages.

**Solution:**
```cmd
REM Option 1: Install Visual C++ Build Tools
REM Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

REM Option 2: Skip packages that need it
REM Edit requirements.txt and remove:
REM - pytesseract (optional)
```

### Issue 4: "error: Microsoft Visual C++ 14.0 or greater is required"

**Solution:**
Install Visual Studio Build Tools:
1. Download: https://visualstudio.microsoft.com/downloads/
2. Install "Desktop development with C++"
3. Restart your computer
4. Try installation again

### Issue 5: FAISS Installation Fails

**Solutions to try (in order):**

```cmd
REM Method 1: No cache
pip install faiss-cpu --no-cache-dir

REM Method 2: Specific version
pip install faiss-cpu==1.7.4

REM Method 3: Use conda (if you have Anaconda)
conda install -c conda-forge faiss-cpu

REM Method 4: Simplified (just for testing)
REM Skip FAISS for now - the app will work without document search
REM Comment out these lines in backend/app/services/document_service.py:
REM - from langchain_community.vectorstores import FAISS
REM - All FAISS-related code
```

### Issue 6: "venv\Scripts\activate" not working in PowerShell

**Solution:**
```powershell
REM Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

REM Then activate
venv\Scripts\Activate.ps1
```

### Issue 7: Port 8000 already in use

**Solution:**
```cmd
REM Find what's using port 8000
netstat -ano | findstr :8000

REM Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

REM Or change the port in backend/main.py:
REM Change port=8000 to port=8001
```

### Issue 8: npm install fails with errors

**Solutions:**

```cmd
REM Method 1: Clear cache
npm cache clean --force
npm install

REM Method 2: Use legacy peer deps
npm install --legacy-peer-deps

REM Method 3: Delete and reinstall
rmdir /s /q node_modules
del package-lock.json
npm install

REM Method 4: Try yarn instead
npm install -g yarn
yarn install
```

### Issue 9: "Cannot find module 'X'" errors

**Solution:**
```cmd
REM Backend:
cd backend
venv\Scripts\activate
pip install --force-reinstall -r requirements.txt

REM Frontend:
cd frontend
rmdir /s /q node_modules
npm install
```

### Issue 10: OpenAI API Error "Invalid API Key"

**Solution:**
1. Check `backend\.env` file
2. Make sure format is: `OPENAI_API_KEY=sk-proj-your-key-here`
3. No spaces around `=`
4. No quotes needed
5. Get new key: https://platform.openai.com/api-keys

---

## 🎯 Minimal Installation (If All Else Fails)

If you're having too many issues, here's a minimal setup that works:

### Step 1: Backend (Minimal)

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn openai python-dotenv
```

Create a simple `main_simple.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/api/chat/message")
async def chat(message: dict):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message["message"]}]
    )
    return {"message": response.choices[0].message.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run it:
```cmd
python main_simple.py
```

### Step 2: Frontend (Use as is)

```cmd
cd frontend
npm install
npm run dev
```

This gives you a working chat without document upload, which is perfect for testing!

---

## 🔧 System Requirements Check

Run these commands to check your system:

```cmd
REM Check Python
python --version
REM Should be 3.10 or higher

REM Check pip
pip --version

REM Check Node.js
node --version
REM Should be 18 or higher

REM Check npm
npm --version

REM Check if OpenAI key works
python -c "import openai; print('OpenAI module OK')"
```

---

## 📞 Still Having Issues?

### Check these:

1. **Antivirus/Firewall**: Sometimes blocks installations
   - Temporarily disable and try again

2. **Admin Rights**: Run Command Prompt as Administrator
   - Right-click → Run as Administrator

3. **Internet Connection**: Some packages are large
   - Make sure you have stable internet

4. **Disk Space**: Need at least 1GB free
   - Check with `dir` command

5. **Windows Version**: 
   ```cmd
   winver
   ```
   Should be Windows 11 (build 22000+)

---

## ✅ Verification Checklist

After setup, verify everything works:

```cmd
REM Backend check
cd backend
venv\Scripts\activate
python -c "import fastapi; import openai; print('Backend OK')"

REM Frontend check
cd frontend
npm run dev
REM Should start without errors
```

---

## 🎯 Quick Commands Reference

```cmd
REM Start Backend
cd backend
venv\Scripts\activate
python main.py

REM Start Frontend (NEW terminal)
cd frontend
npm run dev

REM Stop servers
Ctrl + C

REM Deactivate venv
deactivate
```

---

## 💡 Pro Tips for Windows

1. **Use Windows Terminal** (better than cmd)
   - Install from Microsoft Store
   
2. **Use VS Code** for editing
   - Better than Notepad
   
3. **Keep terminals open**
   - Don't close backend terminal when starting frontend
   
4. **Use Git Bash** (alternative)
   - More Linux-like commands

---

**Need more help?** Check the main SETUP_GUIDE.md or README.md!

**Working now?** Great! Start uploading documents and asking questions! 🎉
