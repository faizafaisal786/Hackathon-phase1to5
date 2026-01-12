#!/bin/bash

echo "================================================"
echo "  Deploying to Minikube"
echo "================================================"
echo ""

cd "$(dirname "$0")"

echo "[1/7] Checking Minikube status..."
if ! minikube status > /dev/null 2>&1; then
    echo "Minikube is not running. Starting Minikube..."
    minikube start
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to start Minikube"
        exit 1
    fi
else
    echo "Minikube is already running!"
fi
echo ""

echo "[2/7] Setting Docker environment to Minikube..."
eval $(minikube docker-env)
echo ""

echo "[3/7] Building Docker images in Minikube..."
echo "Building backend..."
docker build -t todo-backend:latest -f backend/Dockerfile .
if [ $? -ne 0 ]; then
    echo "ERROR: Backend build failed"
    exit 1
fi
echo ""

echo "Building frontend..."
docker build -t todo-frontend:latest ./frontend
if [ $? -ne 0 ]; then
    echo "ERROR: Frontend build failed"
    exit 1
fi
echo ""

echo "[4/7] Applying Kubernetes manifests..."
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
echo ""

echo "[5/7] Waiting for deployments to be ready..."
kubectl rollout status deployment/todo-backend
kubectl rollout status deployment/todo-frontend
echo ""

echo "[6/7] Getting service URLs..."
echo ""
minikube service todo-frontend --url
echo ""

echo "[7/7] Deployment complete!"
echo ""
echo "================================================"
echo "  Access your application:"
echo "  Run: minikube service todo-frontend"
echo ""
echo "  Or get the URL:"
echo "  minikube service todo-frontend --url"
echo ""
echo "  Check status:"
echo "  kubectl get pods"
echo "  kubectl get services"
echo "================================================"
echo ""
