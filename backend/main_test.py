"""
Minimal Test Server
===================
A simplified version to test if basic setup works.
Use this if you're having trouble with the full version.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="AutoQuery Test Server")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("\n⚠️  WARNING: No OpenAI API key found in .env file!")
    print("The server will start but chat won't work.\n")
    client = None
else:
    try:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing OpenAI: {e}")
        client = None

@app.get("/")
def root():
    return {
        "message": "AutoQuery Test Server is running! 🚀",
        "status": "active",
        "openai_configured": client is not None,
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "openai": "configured" if client else "not configured"
    }

@app.post("/api/chat/message")
async def chat(data: dict):
    """Simple chat endpoint for testing"""
    
    if not client:
        return {
            "message": "❌ OpenAI API key not configured. Please add it to backend/.env file.",
            "session_id": "test"
        }
    
    try:
        message = data.get("message", "")
        
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are AutoQuery, a helpful AI assistant."},
                {"role": "user", "content": message}
            ],
            max_tokens=500
        )
        
        return {
            "message": response.choices[0].message.content,
            "session_id": data.get("session_id", "default")
        }
    
    except Exception as e:
        return {
            "message": f"❌ Error: {str(e)}",
            "session_id": "test"
        }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  Starting AutoQuery Test Server")
    print("="*60)
    print("\n✅ Server will start on: http://localhost:8000")
    print("✅ API docs available at: http://localhost:8000/docs")
    print("✅ Press Ctrl+C to stop\n")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main_test:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
