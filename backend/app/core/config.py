"""
Configuration Management
========================
This file handles all environment variables and settings.
Uses python-dotenv to load .env file.

Simple explanation: This reads your API keys from .env file!
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os

class Settings(BaseSettings):
    """
    Application Settings
    All these values are read from .env file
    """
    
    # OpenAI API Key (REQUIRED!)
    OPENAI_API_KEY: str = ""
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Frontend URL for CORS
    FRONTEND_URL: str = "http://localhost:5173"
    
    # OpenAI Model settings
    MODEL_NAME: str = "gpt-4"  # or "gpt-3.5-turbo" for cheaper option
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".docx", ".txt", ".doc"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields

# Cache the settings (load only once)
@lru_cache()
def get_settings() -> Settings:
    """
    Returns cached settings instance
    This is a FastAPI best practice - prevents reading .env multiple times
    """
    settings = Settings()
    
    # Validate OpenAI key
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "":
        print("\n" + "="*60)
        print("⚠️  WARNING: No OpenAI API key found!")
        print("="*60)
        print("\nPlease add your OpenAI API key to backend/.env file:")
        print("OPENAI_API_KEY=sk-your-key-here")
        print("\nGet your key from: https://platform.openai.com/api-keys")
        print("="*60 + "\n")
    
    return settings

# For easy import
settings = get_settings()
