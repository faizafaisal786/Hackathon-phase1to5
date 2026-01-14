@echo off
REM Start Kafka infrastructure with Docker Compose (Windows)
REM Usage: scripts\start-kafka.bat

echo ==========================================
echo Starting Kafka Event-Driven Infrastructure
echo ==========================================

REM Check if Docker is running
docker info > nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker first.
    exit /b 1
)

REM Navigate to project root
cd /d "%~dp0.."

echo.
echo Building and starting services...
echo.

REM Start infrastructure first
docker-compose -f docker-compose.kafka.yml up -d zookeeper redis

echo Waiting for Zookeeper and Redis...
timeout /t 5 /nobreak > nul

REM Start Kafka
docker-compose -f docker-compose.kafka.yml up -d kafka

echo Waiting for Kafka to be ready...
timeout /t 10 /nobreak > nul

REM Initialize Kafka topics
docker-compose -f docker-compose.kafka.yml up kafka-init

REM Start application services
echo.
echo Starting application services...
docker-compose -f docker-compose.kafka.yml up -d backend backend-dapr reminder-service reminder-dapr

echo.
echo Waiting for services to initialize...
timeout /t 10 /nobreak > nul

REM Start frontend
docker-compose -f docker-compose.kafka.yml up -d frontend

REM Start Kafka UI (optional monitoring)
docker-compose -f docker-compose.kafka.yml up -d kafka-ui

echo.
echo ==========================================
echo Services Started Successfully!
echo ==========================================
echo.
echo Available endpoints:
echo   - Frontend:         http://localhost:3000
echo   - Backend API:      http://localhost:8000
echo   - Reminder Service: http://localhost:8001
echo   - Kafka UI:         http://localhost:8080
echo.
echo To view logs:
echo   docker-compose -f docker-compose.kafka.yml logs -f
echo.
echo To stop all services:
echo   docker-compose -f docker-compose.kafka.yml down
echo.
