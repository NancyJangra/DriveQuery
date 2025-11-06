# 🚗 DriveQuery - AI Vehicle Manual Assistant

Your intelligent assistant for vehicle manuals, service guides, and repair documentation.


## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/NancyJangra/DriveQuery.git
cd drivequery
```

### 2. Set Up Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get your key from: https://platform.openai.com/api-keys
```

### 3. Install Backend Dependencies
```bash
cd backend
pip install -r requirements-minimal.txt
# Or use: pip install -r requirements.txt (full version)
```

### 4. Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
# Or: uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Visit: `http://localhost:5173`

## 📦 Project Structure

```
drivequery/
├── .env.example          # Template for environment variables
├── .gitignore           # Protects sensitive files
├── GITHUB_SAFETY.md     # Security guide
├── README.md            # This file
├── backend/
│   ├── requirements.txt          # Full dependencies
│   ├── requirements-minimal.txt  # Minimal setup
│   ├── main.py
│   └── app/
│       ├── api/
│       ├── services/
│       └── core/
└── frontend/
    ├── package.json
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   └── components/
    └── public/
```

## 🔑 Environment Variables

Required variables (see `.env.example`):
- `OPENAI_API_KEY` - Your OpenAI API key
- `VITE_API_URL` - Backend URL (default: http://localhost:8000)

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- OpenAI GPT-4 (AI responses)
- LangChain (Document processing)
- FAISS (Vector search)

**Frontend:**
- React + Vite
- Modern CSS with animations
- Responsive design

## 📝 Features

- ✅ Upload PDF/DOCX vehicle manuals
- ✅ Ask questions in natural language
- ✅ AI-powered responses using GPT-4
- ✅ Document context search
- ✅ Beautiful, responsive UI
- ✅ Real-time chat interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. **Never commit `.env` files**
5. Submit a pull request


## 🆘 Troubleshooting

### "No module named 'openai'"
```bash
pip install -r requirements-minimal.txt
```

### "API key not found"
- Make sure `.env` file exists in root
- Verify `OPENAI_API_KEY` is set
- Restart the backend server

### Port already in use
```bash
# Backend: Change port in .env or use:
uvicorn main:app --port 8001

# Frontend: Use:
npm run dev -- --port 3001
```

## 🔗 Links

- [OpenAI Platform](https://platform.openai.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)

---

