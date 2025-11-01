#!/bin/bash

# MBE Study System - Startup Script
# Starts both backend and frontend servers

echo "🎓 Starting MBE Study System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Start backend
echo "${BLUE}Starting Backend Server...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Start Flask server in background
python app.py &
BACKEND_PID=$!
echo "${GREEN}✓ Backend started on http://localhost:5000 (PID: $BACKEND_PID)${NC}"

cd ..

# Start frontend
echo ""
echo "${BLUE}Starting Frontend Server...${NC}"
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start Vite dev server
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "${GREEN}✓ MBE Study System is running!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Frontend: http://localhost:3002"
echo "🔌 Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✓ Servers stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for both processes
wait
