# 🪟 AutoQuery for Windows 11 - UPDATED!

## ✅ What's Fixed

I've updated the project specifically for Windows 11:

1. ✅ **Updated requirements.txt** - Compatible versions for Windows
2. ✅ **Added setup-windows.bat** - Automatic installation script
3. ✅ **Added WINDOWS_INSTALL.md** - Step-by-step Windows guide
4. ✅ **Added WINDOWS_SETUP.md** - Troubleshooting for Windows
5. ✅ **Added requirements-minimal.txt** - Easier installation option

---

## 🚀 Quick Start for Windows 11

### Option 1: Automatic Setup (Easiest!)

1. **Extract the ZIP file**
2. **Double-click** `setup-windows.bat`
3. **Follow the instructions**

That's it! The script does everything automatically.

### Option 2: Manual Setup (Step-by-Step)

**Read this file:** `WINDOWS_INSTALL.md`

It has detailed step-by-step instructions with screenshots!

---

## 📋 What You Need

Before starting:

1. **Python 3.10 or higher**
   - Download: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation

2. **Node.js 18 or higher**
   - Download: https://nodejs.org/
   - Install the LTS version

3. **OpenAI API Key**
   - Get it: https://platform.openai.com/api-keys
   - Free $5 credits available!

---

## 🎯 Installation Methods

### Method 1: Use Minimal Requirements (Fastest)

If you're having issues with the full installation:

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements-minimal.txt
```

This installs only essential packages - easier and faster!

### Method 2: Full Installation

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ⚠️ Common Windows Errors - Quick Fixes

### "python is not recognized"
→ **Fix:** Install Python with "Add to PATH" checked

### "Microsoft Visual C++ required"
→ **Fix:** Use `requirements-minimal.txt` instead

### "FAISS won't install"
→ **Fix:** Skip it! Use minimal version. Document search is optional.

### "Port 8000 already in use"
→ **Fix:** `netstat -ano | findstr :8000` then `taskkill /PID <number> /F`

**Full troubleshooting:** See `WINDOWS_SETUP.md`

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **WINDOWS_INSTALL.md** | ⭐ Start here! Step-by-step Windows guide |
| **WINDOWS_SETUP.md** | Detailed troubleshooting for Windows |
| **setup-windows.bat** | Automatic installation script |
| START_HERE.md | General project overview |
| SETUP_GUIDE.md | Original setup guide (all platforms) |

---

## ✅ Testing After Installation

### Test Backend:
```cmd
cd backend
venv\Scripts\activate
python main.py
```

Should see: `Uvicorn running on http://0.0.0.0:8000`

### Test Frontend (in NEW terminal):
```cmd
cd frontend
npm run dev
```

Should see: `Local: http://localhost:5173/`

### Test in Browser:
Open: http://localhost:5173

You should see AutoQuery! 🎉

---

## 🎯 Quick Commands

```cmd
# Start Backend
cd backend
venv\Scripts\activate
python main.py

# Start Frontend (NEW terminal)
cd frontend
npm run dev

# Stop (in each terminal)
Ctrl + C
```

---

## 💡 Tips for Windows Users

1. **Use two Command Prompt windows** - One for backend, one for frontend
2. **Don't close backend terminal** when starting frontend
3. **Add to Windows Defender exceptions** if it blocks installations
4. **Run as Administrator** if you get permission errors

---

## 📁 Updated Files

New/Updated files in this version:
- ✅ `backend/requirements.txt` (Windows-compatible versions)
- ✅ `backend/requirements-minimal.txt` (Easier installation)
- ✅ `setup-windows.bat` (Auto setup script)
- ✅ `WINDOWS_INSTALL.md` (Step-by-step guide)
- ✅ `WINDOWS_SETUP.md` (Troubleshooting)
- ✅ `README_WINDOWS.md` (This file!)

---

## 🆘 Still Having Issues?

### Step 1: Try Minimal Installation
```cmd
cd backend
pip install -r requirements-minimal.txt
```

### Step 2: Read Troubleshooting
Open: `WINDOWS_SETUP.md`

### Step 3: Check Documentation
Open: `WINDOWS_INSTALL.md`

---

## 🎉 Success Checklist

- [ ] Python installed (check: `python --version`)
- [ ] Node.js installed (check: `node --version`)
- [ ] Backend runs without errors
- [ ] Frontend runs without errors
- [ ] Can open http://localhost:5173
- [ ] Can send chat messages
- [ ] OpenAI API key added to .env

---

## 🚀 Once It's Working

1. Upload documents (PDF, DOCX, TXT)
2. Ask questions about them
3. Get AI-powered answers
4. Add to your resume! 🎯

---

**Made specifically for Windows 11 users! Good luck! 🎉**

For detailed instructions, open **WINDOWS_INSTALL.md**
