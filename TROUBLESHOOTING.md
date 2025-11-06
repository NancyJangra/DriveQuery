# 🔧 Troubleshooting Guide

Common issues and how to fix them!

---

## ❌ Backend Issues

### Issue: "OPENAI_API_KEY not found"

**Symptom:**
```
⚠️  WARNING: OPENAI_API_KEY not found in environment variables!
```

**Solution:**
1. Create a file named `.env` in the `backend` folder (not `.env.txt`!)
2. Add this line (with your actual key):
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
3. Restart the backend server

---

### Issue: "Module not found" errors

**Symptom:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If that doesn't work:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

### Issue: "Port 8000 already in use"

**Symptom:**
```
Error: [Errno 48] Address already in use
```

**Solution:**

**On Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**On Mac/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

Or change the port in the command:
```bash
uvicorn app.main:app --reload --port 8001
```

---

### Issue: Virtual environment not activating

**Symptom:**
You don't see `(venv)` in your terminal

**Solution:**

**Windows:**
```bash
cd backend
venv\Scripts\activate
```

**Mac/Linux:**
```bash
cd backend
source venv/bin/activate
```

If still not working, recreate it:
```bash
rm -rf venv  # Windows: rmdir /s venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### Issue: "Can't import docx"

**Symptom:**
```
ModuleNotFoundError: No module named 'docx'
```

**Solution:**
```bash
pip install python-docx
```

Note: It's `python-docx` but imported as `docx`!

---

## ❌ Frontend Issues

### Issue: "npm: command not found"

**Symptom:**
```
bash: npm: command not found
```

**Solution:**
Install Node.js from https://nodejs.org/

After installation, restart your terminal and try again.

---

### Issue: "Cannot find module '@/lib/utils'"

**Symptom:**
```
Error: Cannot find module '@/lib/utils'
```

**Solution:**
This is a path alias issue. Make sure:
1. `tsconfig.json` has the paths configuration
2. Run `npm install` again
3. Restart Vite dev server

---

### Issue: "Port 5173 already in use"

**Symptom:**
```
Port 5173 is in use, trying another one...
```

**Solution:**

**Option 1:** Kill the process
```bash
# Mac/Linux:
lsof -ti:5173 | xargs kill -9

# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F
```

**Option 2:** Use a different port
Edit `vite.config.ts`:
```typescript
server: {
  port: 3000,  // Change to any available port
}
```

---

### Issue: Blank white screen

**Symptom:**
Browser shows empty white page, no errors in console

**Solution:**
1. Check browser console (F12) for errors
2. Make sure backend is running
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try opening in incognito/private mode
5. Check if `http://localhost:8000/docs` works

---

### Issue: "Failed to fetch" or CORS errors

**Symptom:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Make sure backend is running on port 8000
2. Check `backend/app/main.py` has CORS middleware
3. Try restarting both servers
4. Clear browser cache

---

## ❌ File Upload Issues

### Issue: Can't upload files

**Symptom:**
Upload button doesn't work or gives errors

**Solution:**
1. Check file type (only PDF and DOCX supported)
2. Check file size (max 10MB)
3. Make sure `backend/uploads` folder exists:
   ```bash
   mkdir backend/uploads
   ```
4. Check backend logs for errors

---

### Issue: "Unsupported file type"

**Symptom:**
```
Error: Unsupported file type: .doc
```

**Solution:**
- Only `.pdf` and `.docx` are supported
- For older `.doc` files, open in Word and save as `.docx`
- Images: Not directly supported (would need OCR)

---

### Issue: PDF text extraction returns gibberish

**Symptom:**
Uploaded PDF but extracted text is symbols/garbage

**Solution:**
- PDF might be scanned image (not text-based)
- Try using a different PDF
- For scanned PDFs, you'd need OCR (pytesseract) - advanced feature

---

## ❌ OpenAI API Issues

### Issue: "Rate limit exceeded"

**Symptom:**
```
Error: Rate limit reached for requests
```

**Solution:**
- Wait a few minutes
- You've hit your API quota
- Check your OpenAI account for usage
- Consider upgrading your OpenAI plan

---

### Issue: "Invalid API key"

**Symptom:**
```
Error: Incorrect API key provided
```

**Solution:**
1. Check your API key at https://platform.openai.com/api-keys
2. Make sure there are no extra spaces in `.env` file
3. Format should be: `OPENAI_API_KEY=sk-...` (no spaces around `=`)
4. Restart backend after changing `.env`

---

### Issue: "Model not found"

**Symptom:**
```
Error: The model 'gpt-4' does not exist
```

**Solution:**
1. You might not have access to GPT-4
2. Change model in `backend/app/services/chat_service.py`:
   ```python
   self.model = "gpt-3.5-turbo"  # Instead of "gpt-4"
   ```
3. GPT-3.5 is cheaper and faster!

---

## ❌ General Issues

### Issue: Changes not reflecting

**Symptom:**
Made code changes but nothing happens

**Solution:**

**Backend:**
- Make sure `--reload` flag is used
- Restart the server manually
- Check for syntax errors in terminal

**Frontend:**
- Vite should auto-reload
- Try refreshing browser (Ctrl+R or Cmd+R)
- Check browser console for errors
- Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

---

### Issue: "Connection refused"

**Symptom:**
```
Error: connect ECONNREFUSED 127.0.0.1:8000
```

**Solution:**
1. Backend is not running - start it!
2. Check if backend is on port 8000:
   ```bash
   curl http://localhost:8000/health
   ```
3. Check firewall settings

---

### Issue: Slow responses

**Symptom:**
Takes 30+ seconds to get AI response

**Solution:**
- This is normal for GPT-4! It thinks deeply
- Use GPT-3.5-turbo for faster responses
- Check your internet connection
- Large documents take longer to process

---

## 🔍 Debugging Tips

### 1. Check Logs

**Backend logs:**
Look at the terminal running the backend server. It shows:
- Incoming requests
- Errors
- API calls

**Frontend logs:**
Open browser console (F12) and check:
- Network tab for API calls
- Console tab for JavaScript errors

### 2. Test Backend Separately

Open http://localhost:8000/docs in your browser.
Try the endpoints manually to see if backend works.

### 3. Test Individual Components

Comment out parts of code to isolate the issue:
```typescript
// Try commenting this out to test
// setMessages(prev => [...prev, aiMessage])
console.log('Response:', aiMessage)
```

### 4. Check File Permissions

Make sure you have write permissions:
```bash
ls -la backend/uploads/
chmod 755 backend/uploads/
```

---

## 📞 Still Stuck?

### Before asking for help:

1. ✅ Read the error message carefully
2. ✅ Check this troubleshooting guide
3. ✅ Search Google for the error
4. ✅ Check if both servers are running
5. ✅ Try restarting everything

### When asking for help:

Include:
- Operating system (Windows/Mac/Linux)
- Python version (`python --version`)
- Node version (`node --version`)
- Full error message
- What you were trying to do
- What you've already tried

---

## ✅ Quick Health Check

Run these commands to verify everything:

```bash
# 1. Check Python
python --version

# 2. Check Node
node --version

# 3. Check backend health
curl http://localhost:8000/health

# 4. Check frontend
curl http://localhost:5173

# 5. Test OpenAI (in Python)
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

All should return success!

---

## 💡 Prevention Tips

1. **Always activate virtual environment** before running backend
2. **Keep dependencies updated** (but test after updating!)
3. **Use Git** to track changes (easy to revert!)
4. **Read error messages** - they usually tell you exactly what's wrong
5. **Test incrementally** - Don't change too much at once

---

Remember: Every developer faces these issues! You're doing great! 🚀
