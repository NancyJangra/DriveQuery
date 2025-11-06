@echo off
REM AutoQuery - Quick Start Script for Windows
REM This script helps you start both backend and frontend together

echo 🚀 Starting AutoQuery...
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ❌ Error: Please run this script from the autoquery root directory
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Error: Please run this script from the autoquery root directory
    pause
    exit /b 1
)

REM Check if .env exists
if not exist "backend\.env" (
    echo ⚠️  Warning: backend\.env file not found!
    echo    Please create it with your OpenAI API key:
    echo    OPENAI_API_KEY=your-key-here
    echo.
    pause
    exit /b 1
)

echo ✅ Environment file found
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo ⚠️  Virtual environment not found. Creating one...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
    echo ✅ Virtual environment created and packages installed
    echo.
)

REM Check if node_modules exists
if not exist "frontend\node_modules" (
    echo ⚠️  Node modules not found. Installing...
    cd frontend
    call npm install
    cd ..
    echo ✅ Node modules installed
    echo.
)

echo 🎯 Starting Backend (FastAPI)...
echo    Backend will run on: http://localhost:8000
echo.

REM Start backend in new window
start "AutoQuery Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak > nul
echo.

echo 🎯 Starting Frontend (React)...
echo    Frontend will run on: http://localhost:5173
echo.

REM Start frontend in new window
start "AutoQuery Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ AutoQuery is running!
echo.
echo 📝 URLs:
echo    • Chat Interface: http://localhost:5173
echo    • API Docs: http://localhost:8000/docs
echo.
echo Close both terminal windows to stop the servers
echo.
pause
