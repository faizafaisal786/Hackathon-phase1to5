@echo off
echo ================================================
echo   Starting Todo App Frontend
echo ================================================
echo.

cd /d "%~dp0frontend"

echo [1/3] Checking Node.js installation...
node --version
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo.

echo [2/3] Installing/Updating dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/3] Starting development server...
echo.
echo ================================================
echo   Frontend will be available at:
echo   http://localhost:3000
echo.
echo   Make sure the backend is running at:
echo   http://localhost:8000
echo.
echo   Press CTRL+C to stop the server
echo ================================================
echo.

call npm run dev
