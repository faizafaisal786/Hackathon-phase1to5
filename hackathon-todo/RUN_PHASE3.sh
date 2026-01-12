#!/bin/bash

echo "========================================"
echo "Phase 3 - Todo App with AI Chat"
echo "========================================"
echo ""
echo "Step 1: Starting Backend + AI..."
echo ""

cd backend
# Start backend in background
uvicorn main:app --reload &
BACKEND_PID=$!

echo "Backend + AI running on http://localhost:8000 (PID: $BACKEND_PID)"
echo ""

# Wait a moment for backend to start
sleep 3

echo "Step 2: Starting Frontend..."
echo ""

cd ../frontend
# Start frontend in background
npm run dev &
FRONTEND_PID=$!

echo "Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""

echo "========================================"
echo "Both servers are running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "========================================"
echo ""
echo "Open http://localhost:3000/chat in your browser"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
wait
