@echo off
REM AutoQuery Windows Setup Script
REM ===============================
REM This script will set up the entire project on Windows 11

echo.
echo ========================================
echo   AutoQuery Setup for Windows 11
echo ========================================
echo.

REM Check Python installation
echo [1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)
echo Python found!

REM Check Node.js installation
echo.
echo [2/8] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from nodejs.org
    pause
    exit /b 1
)
echo Node.js found!

REM Setup Backend
echo.
echo [3/8] Setting up Python Backend...
cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python packages
echo.
echo [4/8] Installing Python packages (this may take 3-5 minutes)...
pip install --no-cache-dir -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install some packages
    echo Trying with simpler installation method...
    pip install fastapi uvicorn openai langchain python-dotenv PyPDF2 python-docx
    pip install faiss-cpu --no-cache-dir
)

REM Create .env file if it doesn't exist
echo.
echo [5/8] Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit backend\.env and add your OpenAI API key!
    echo Get your key from: https://platform.openai.com/api-keys
    echo.
) else (
    echo .env file already exists
)

REM Create necessary directories
echo Creating upload directories...
if not exist uploads mkdir uploads
if not exist vector_store mkdir vector_store

cd ..

REM Setup Frontend
echo.
echo [6/8] Setting up React Frontend...
cd frontend

REM Install npm packages
echo Installing npm packages (this may take 2-3 minutes)...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install npm packages
    echo Trying to clear cache and reinstall...
    call npm cache clean --force
    call npm install
)

REM Create .env file if it doesn't exist
echo.
echo [7/8] Setting up frontend environment...
if not exist .env (
    copy .env.example .env
    echo Frontend .env created
) else (
    echo Frontend .env already exists
)

cd ..

REM Final instructions
echo.
echo ========================================
echo   Setup Complete! 🎉
echo ========================================
echo.
echo [8/8] Next Steps:
echo.
echo 1. Edit backend\.env and add your OpenAI API key
echo    Get it from: https://platform.openai.com/api-keys
echo.
echo 2. To start the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 3. To start the frontend (in a NEW terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open browser: http://localhost:5173
echo.
echo For detailed instructions, read SETUP_GUIDE.md
echo.
echo Press any key to exit...
pause >nul
