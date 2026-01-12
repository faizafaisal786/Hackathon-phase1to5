@echo off
echo ================================================
echo   Starting Todo App Backend Server
echo ================================================
echo.

cd /d "%~dp0backend"

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo.

echo [2/3] Installing/Updating dependencies...
pip install -r ../requirements.txt --quiet
if errorlevel 1 (
    echo WARNING: Some dependencies may have failed to install
    echo Continuing anyway...
)
echo.

echo [3/3] Starting backend server...
echo.
echo ================================================
echo   Server will be available at:
echo   http://localhost:8000
echo.
echo   API Endpoints:
echo   - http://localhost:8000/api/chat
echo   - http://localhost:8000/api/tasks
echo   - http://localhost:8000/docs (API documentation)
echo.
echo   Press CTRL+C to stop the server
echo ================================================
echo.

python main.py
