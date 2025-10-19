#!/bin/bash

# SmartKart Pro - Startup Script
echo "🚀 Starting SmartKart Pro..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 Installing Python dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment variables..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your SerpAPI key!"
    echo "   Current key: 8583174e1f99fae5aa5dfbef52b8c70d4e3ee6fb419d0d5ae0e017d6bbfe8636"
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "🎯 Starting services..."
echo ""

# Start backend
echo "🐍 Starting Backend (FastAPI) on http://localhost:8000..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "⚛️  Starting Frontend (React) on http://localhost:8080..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ SmartKart Pro is running!"
echo ""
echo "📱 Frontend: http://localhost:8080"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Function to handle cleanup
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "👋 SmartKart Pro stopped. Goodbye!"
    exit 0
}

# Set trap to handle Ctrl+C
trap cleanup SIGINT SIGTERM

# Wait for services
wait $BACKEND_PID $FRONTEND_PID
