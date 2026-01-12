#!/bin/bash

echo "================================================"
echo "  Starting Todo App Frontend"
echo "================================================"
echo ""

cd "$(dirname "$0")/frontend"

echo "[1/3] Checking Node.js installation..."
node --version
if [ $? -ne 0 ]; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi
echo ""

echo "[2/3] Installing/Updating dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

echo "[3/3] Starting development server..."
echo ""
echo "================================================"
echo "  Frontend will be available at:"
echo "  http://localhost:3000"
echo ""
echo "  Make sure the backend is running at:"
echo "  http://localhost:8000"
echo ""
echo "  Press CTRL+C to stop the server"
echo "================================================"
echo ""

npm run dev
