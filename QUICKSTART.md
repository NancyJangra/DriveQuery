# ⚡ Quick Start (For Experienced Developers)

Get AutoQuery running in 5 minutes!

## Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API Key

## Setup

### 1. Backend (Terminal 1)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python main.py
```

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 3. Open Browser
http://localhost:5173

## Test It
1. Upload a document (PDF/DOCX/TXT)
2. Ask: "What is this document about?"
3. Get AI-powered answer!

## API Endpoints

### Chat
```bash
POST http://localhost:8000/api/chat/message
{
  "message": "What is X?",
  "session_id": "user123",
  "use_documents": true
}
```

### Upload Document
```bash
POST http://localhost:8000/api/documents/upload
Content-Type: multipart/form-data
file: <file>
```

### List Documents
```bash
GET http://localhost:8000/api/documents/list
```

## Architecture

```
User Question
    ↓
Frontend (React)
    ↓
FastAPI Backend
    ↓
FAISS Search → Relevant Chunks
    ↓
OpenAI GPT-4 (with context)
    ↓
Answer
```

## Tech Stack
- **Frontend**: React, TypeScript, Vite, Tailwind, shadcn-ui
- **Backend**: FastAPI, LangChain, FAISS, OpenAI
- **Processing**: PyPDF2, python-docx, pytesseract

## Common Issues

**FAISS error?**
```bash
pip install faiss-cpu --no-cache-dir
```

**CORS error?**
- Check both servers are running
- Verify .env files

**OpenAI error?**
- Verify API key in backend/.env
- Check credits at platform.openai.com

## Documentation
- Full README: [README.md](README.md)
- Detailed Setup: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- API Docs: http://localhost:8000/docs

---

That's it! Now go build something awesome! 🚀
