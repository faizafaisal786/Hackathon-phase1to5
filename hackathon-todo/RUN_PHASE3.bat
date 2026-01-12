@echo off
echo ========================================
echo Phase 3 - Todo App with AI Chat
echo ========================================
echo.
echo Step 1: Starting Backend + AI...
echo.
cd backend
start cmd /k "echo Backend + AI running on http://localhost:8000 && uvicorn main:app --reload"
timeout /t 3 /nobreak > nul
echo.
echo Step 2: Starting Frontend...
echo.
cd ..\frontend
start cmd /k "echo Frontend running on http://localhost:3000 && npm run dev"
echo.
echo ========================================
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Open http://localhost:3000/chat in your browser
echo.
pause
