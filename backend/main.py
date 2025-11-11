
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Rest of your imports...
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import our API routes
from app.api import chat, documents

# Create the FastAPI application
app = FastAPI(
    title="AutoQuery API",
    description="AI-Powered Vehicle Manual Assistant - Upload manuals and ask questions!",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows your frontend (React) to talk to your backend (FastAPI)
# In production, you'd want to specify exact origins instead of "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
        "http://localhost:5173",
        "https://NancyJangra.github.io"],  # Allows all origins - fine for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include API routers
# These handle the actual endpoints for chat and documents
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(documents.router, prefix="/api", tags=["documents"])

# Serve uploaded files as static files
# This allows the frontend to access uploaded documents if needed
upload_dir = "uploads"
if os.path.exists(upload_dir):
    app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# Root endpoint - health check
@app.get("/", tags=["default"])
async def root():
    """
    Root endpoint - shows the API is running
    Visit http://localhost:8000 to see this
    """
    return {
        "status": "running",
        "message": "AutoQuery Backend is running! 🚗",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "upload": "/documents/upload",
            "list": "/documents/list",
            "chat": "/chat"
        }
    }

@app.get("/health", tags=["default"])
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "message": "All systems operational"
    }

# This runs when you execute: python main.py
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting AutoQuery Backend Server...")
    print("="*60)
    print(f"📍 Server URL:        http://localhost:8000")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"📋 Alternative Docs:  http://localhost:8000/redoc")
    print("="*60)
    print("💡 Tip: Keep this terminal running!")
    print("🛑 To stop: Press Ctrl+C")
    print("="*60 + "\n")
    
    # Run the server with uvicorn
    uvicorn.run(
        "main:app",           # The FastAPI app
        host="0.0.0.0",       # Listen on all network interfaces
        port=8000,            # Port number
        reload=True,          # Auto-reload on code changes (great for development!)
        log_level="info"      # Logging level
    )