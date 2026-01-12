#!/bin/bash

echo "================================================"
echo "  Starting Todo App Backend Server"
echo "================================================"
echo ""

cd "$(dirname "$0")/backend"

echo "[1/3] Checking Python installation..."
python3 --version || python --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi
echo ""

echo "[2/3] Installing/Updating dependencies..."
pip3 install -r ../requirements.txt --quiet 2>/dev/null || pip install -r ../requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "WARNING: Some dependencies may have failed to install"
    echo "Continuing anyway..."
fi
echo ""

echo "[3/3] Starting backend server..."
echo ""
echo "================================================"
echo "  Server will be available at:"
echo "  http://localhost:8000"
echo ""
echo "  API Endpoints:"
echo "  - http://localhost:8000/api/chat"
echo "  - http://localhost:8000/api/tasks"
echo "  - http://localhost:8000/docs (API documentation)"
echo ""
echo "  Press CTRL+C to stop the server"
echo "================================================"
echo ""

python3 main.py || python main.py
