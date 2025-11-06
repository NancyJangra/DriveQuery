#!/bin/bash

# AutoQuery - Quick Start Script
# This script helps you start both backend and frontend together

echo "🚀 Starting AutoQuery..."
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the autoquery root directory"
    exit 1
fi

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Warning: backend/.env file not found!"
    echo "   Please create it with your OpenAI API key:"
    echo "   OPENAI_API_KEY=your-key-here"
    echo ""
    exit 1
fi

echo "✅ Environment file found"
echo ""

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    echo "✅ Virtual environment created and packages installed"
    echo ""
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Node modules not found. Installing..."
    cd frontend
    npm install
    cd ..
    echo "✅ Node modules installed"
    echo ""
fi

echo "🎯 Starting Backend (FastAPI)..."
echo "   Backend will run on: http://localhost:8000"
echo ""

# Start backend in background
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "⏳ Waiting for backend to start..."
sleep 3
echo ""

echo "🎯 Starting Frontend (React)..."
echo "   Frontend will run on: http://localhost:5173"
echo ""

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ AutoQuery is running!"
echo ""
echo "📝 URLs:"
echo "   • Chat Interface: http://localhost:5173"
echo "   • API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
