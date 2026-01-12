@echo off
echo ================================================
echo   Deploying to Minikube
echo ================================================
echo.

cd /d "%~dp0"

echo [1/7] Checking Minikube status...
minikube status >nul 2>&1
if errorlevel 1 (
    echo Minikube is not running. Starting Minikube...
    minikube start
    if errorlevel 1 (
        echo ERROR: Failed to start Minikube
        pause
        exit /b 1
    )
) else (
    echo Minikube is already running!
)
echo.

echo [2/7] Setting Docker environment to Minikube...
@echo on
@FOR /f "tokens=*" %%i IN ('minikube -p minikube docker-env --shell cmd') DO @%%i
@echo off
echo.

echo [3/7] Building Docker images in Minikube...
echo Building backend...
docker build -t todo-backend:latest -f backend/Dockerfile .
if errorlevel 1 (
    echo ERROR: Backend build failed
    pause
    exit /b 1
)
echo.

echo Building frontend...
docker build -t todo-frontend:latest ./frontend
if errorlevel 1 (
    echo ERROR: Frontend build failed
    pause
    exit /b 1
)
echo.

echo [4/7] Applying Kubernetes manifests...
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
echo.

echo [5/7] Waiting for deployments to be ready...
kubectl rollout status deployment/todo-backend
kubectl rollout status deployment/todo-frontend
echo.

echo [6/7] Getting service URLs...
echo.
minikube service todo-frontend --url
echo.

echo [7/7] Deployment complete!
echo.
echo ================================================
echo   Access your application:
echo   Run: minikube service todo-frontend
echo.
echo   Or get the URL:
echo   minikube service todo-frontend --url
echo.
echo   Check status:
echo   kubectl get pods
echo   kubectl get services
echo ================================================
echo.

pause
