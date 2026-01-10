@echo off
REM 🚀 Windows Deployment Script for All Phases
REM Professional Hackathon Todo Project

echo =================================="
echo   HACKATHON TODO - DEPLOYMENT
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed
    exit /b 1
)
echo [OK] Python installed

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed
    exit /b 1
)
echo [OK] Node.js installed

REM Check Vercel CLI
call vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing Vercel CLI...
    call npm install -g vercel
)
echo [OK] Vercel CLI installed

echo.
echo Select deployment option:
echo 1. Deploy Phase 1 (CLI to Web)
echo 2. Test Phase 2 Backend
echo 3. Deploy Phase 2 Frontend
echo 4. Run Phase 4 (Docker)
echo 5. Exit
echo.

set /p choice="Enter choice [1-5]: "

if "%choice%"=="1" goto phase1
if "%choice%"=="2" goto phase2backend
if "%choice%"=="3" goto phase2frontend
if "%choice%"=="4" goto phase4
if "%choice%"=="5" goto end
goto invalid

:phase1
echo.
echo === Phase 1: Deploying to Vercel ===
cd todo-phase1
call vercel --prod --yes
cd ..
echo [SUCCESS] Phase 1 deployed!
goto menu

:phase2backend
echo.
echo === Phase 2: Testing Backend ===
cd hackathon-todo
call python test_app.py
if %errorlevel% equ 0 (
    echo [SUCCESS] All tests passed!
    echo [INFO] Backend ready for deployment
    echo [INFO] Deploy to Railway: railway up
) else (
    echo [ERROR] Tests failed!
)
cd ..
goto menu

:phase2frontend
echo.
echo === Phase 2: Deploying Frontend ===
cd hackathon-todo\frontend
call npm install
call npm run build
if %errorlevel% equ 0 (
    echo [SUCCESS] Build successful!
    call vercel --prod --yes
    echo [SUCCESS] Frontend deployed!
) else (
    echo [ERROR] Build failed!
)
cd ..\..
goto menu

:phase4
echo.
echo === Phase 4: Running Docker ===
cd hackathon-todo
docker-compose up -d
if %errorlevel% equ 0 (
    echo [SUCCESS] Docker containers running!
    echo [INFO] Backend: http://localhost:8000
    echo [INFO] Frontend: http://localhost:3000
) else (
    echo [ERROR] Docker failed!
)
cd ..
goto menu

:invalid
echo [ERROR] Invalid choice
goto menu

:menu
echo.
echo Press any key to return to menu or Ctrl+C to exit...
pause >nul
cls
goto start

:end
echo.
echo Exiting...
exit /b 0
