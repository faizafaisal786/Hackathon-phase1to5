@echo off
echo ================================================
echo   Building Docker Images
echo ================================================
echo.

cd /d "%~dp0"

echo [1/3] Building Backend Image...
docker build -t todo-backend -f backend/Dockerfile .
if errorlevel 1 (
    echo ERROR: Backend build failed
    pause
    exit /b 1
)
echo Backend image built successfully!
echo.

echo [2/3] Building Frontend Image...
docker build -t todo-frontend ./frontend
if errorlevel 1 (
    echo ERROR: Frontend build failed
    pause
    exit /b 1
)
echo Frontend image built successfully!
echo.

echo [3/3] Images Built Successfully!
echo.
echo ================================================
echo   Docker Images Ready:
echo   - todo-backend
echo   - todo-frontend
echo.
echo   To run the containers:
echo   docker-compose up -d
echo ================================================
echo.

pause
