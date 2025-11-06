"""
AutoQuery Backend - Main FastAPI Application
This is the entry point for the backend server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import routes
from app.routes import chat, documents

# Create FastAPI app
app = FastAPI(
    title="AutoQuery API",
    description="AI-Powered Document Q&A Chatbot Backend",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the frontend (React) to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Alternative React port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Include routers (routes for different features)
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])

# Root endpoint - Health check
@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running
    """
    return {
        "message": "AutoQuery API is running! 🚀",
        "version": "1.0.0",
        "docs": "/docs",  # Swagger UI documentation
        "status": "healthy"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy", "service": "AutoQuery Backend"}

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    This runs when the server starts
    """
    print("🚀 AutoQuery Backend is starting...")
    print("📝 API Documentation available at: http://localhost:8000/docs")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables!")
        print("   Please create a .env file with your OpenAI API key")
    else:
        print("✅ OpenAI API key loaded successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    This runs when the server shuts down
    """
    print("👋 AutoQuery Backend is shutting down...")

if __name__ == "__main__":
    import uvicorn
    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes (for development)
    )
