"""
AutoQuery Installation Test Script
===================================
This script tests if all required packages are installed correctly.
Run this after installation to verify everything works!
"""

import sys

print("\n" + "="*60)
print("  AutoQuery Installation Test")
print("="*60 + "\n")

# Test 1: Python Version
print("[1/8] Checking Python version...")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 10:
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - OK")
else:
    print(f"❌ Python {python_version.major}.{python_version.minor} - Need 3.10+")
    sys.exit(1)

# Test 2: FastAPI
print("\n[2/8] Checking FastAPI...")
try:
    import fastapi
    print(f"✅ FastAPI {fastapi.__version__} - OK")
except ImportError:
    print("❌ FastAPI not installed")
    print("   Install: pip install fastapi")

# Test 3: Uvicorn
print("\n[3/8] Checking Uvicorn...")
try:
    import uvicorn
    print(f"✅ Uvicorn - OK")
except ImportError:
    print("❌ Uvicorn not installed")
    print("   Install: pip install uvicorn")

# Test 4: OpenAI
print("\n[4/8] Checking OpenAI...")
try:
    import openai
    print(f"✅ OpenAI {openai.__version__} - OK")
except ImportError:
    print("❌ OpenAI not installed")
    print("   Install: pip install openai")

# Test 5: Document Processing
print("\n[5/8] Checking document processing libraries...")
try:
    import PyPDF2
    print("✅ PyPDF2 - OK")
except ImportError:
    print("❌ PyPDF2 not installed")
    print("   Install: pip install PyPDF2")

try:
    from docx import Document
    print("✅ python-docx - OK")
except ImportError:
    print("❌ python-docx not installed")
    print("   Install: pip install python-docx")

# Test 6: Environment Management
print("\n[6/8] Checking environment management...")
try:
    from dotenv import load_dotenv
    print("✅ python-dotenv - OK")
except ImportError:
    print("❌ python-dotenv not installed")
    print("   Install: pip install python-dotenv")

# Test 7: Pydantic
print("\n[7/8] Checking Pydantic...")
try:
    import pydantic
    print(f"✅ Pydantic {pydantic.__version__} - OK")
except ImportError:
    print("❌ Pydantic not installed")
    print("   Install: pip install pydantic")

# Test 8: Optional - LangChain & FAISS
print("\n[8/8] Checking optional packages (for advanced features)...")
try:
    import langchain
    print(f"✅ LangChain {langchain.__version__} - OK")
except ImportError:
    print("⚠️  LangChain not installed (optional)")
    print("   Install: pip install langchain")

try:
    import faiss
    print("✅ FAISS - OK")
except ImportError:
    print("⚠️  FAISS not installed (optional)")
    print("   Install: pip install faiss-cpu --no-cache-dir")

# Test 9: Check .env file
print("\n[9/9] Checking configuration...")
import os
if os.path.exists(".env"):
    print("✅ .env file exists")
    
    # Try to load and check API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key != "sk-your-openai-api-key-here":
        if api_key.startswith("sk-"):
            print("✅ OpenAI API key configured")
        else:
            print("⚠️  OpenAI API key format looks incorrect")
    else:
        print("❌ OpenAI API key not set in .env")
        print("   Edit .env and add: OPENAI_API_KEY=sk-your-key-here")
else:
    print("❌ .env file not found")
    print("   Copy .env.example to .env")
    print("   Command: copy .env.example .env")

# Summary
print("\n" + "="*60)
print("  Test Summary")
print("="*60)
print("\nCore packages (REQUIRED):")
core_ok = True
try:
    import fastapi, uvicorn, openai, PyPDF2, pydantic
    from docx import Document
    from dotenv import load_dotenv
    print("✅ All core packages installed!")
except ImportError as e:
    print(f"❌ Missing core packages: {e}")
    core_ok = False

print("\nOptional packages (for advanced features):")
try:
    import langchain, faiss
    print("✅ All optional packages installed!")
    print("   → Full document search enabled")
except ImportError:
    print("⚠️  Some optional packages missing")
    print("   → Document search will use simple text matching")
    print("   → To install: pip install langchain faiss-cpu --no-cache-dir")

print("\n" + "="*60)
if core_ok:
    print("✅ Installation successful! You can now run:")
    print("   python main.py")
else:
    print("❌ Some core packages are missing. Please install them:")
    print("   pip install -r requirements-minimal.txt")
print("="*60 + "\n")
