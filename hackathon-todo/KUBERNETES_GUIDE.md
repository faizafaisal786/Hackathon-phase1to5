# ☸️ Kubernetes & Minikube Deployment Guide

Complete guide for deploying the Todo App to Kubernetes using Minikube.

## 📋 Prerequisites

- **Minikube** installed
- **kubectl** installed
- **Docker** installed
- At least 4GB RAM available
- 20GB free disk space

## 🚀 Quick Start

### Using Deployment Script (Recommended)

**Windows:**
```bash
cd hackathon-todo
MINIKUBE_DEPLOY.bat
```

**Linux/Mac:**
```bash
cd hackathon-todo
./MINIKUBE_DEPLOY.sh
```

### Manual Deployment

```bash
# 1. Start Minikube
minikube start

# 2. Use Minikube Docker
eval $(minikube docker-env)

# 3. Build images
docker build -t todo-backend:latest -f backend/Dockerfile .
docker build -t todo-frontend:latest ./frontend

# 4. Deploy
kubectl apply -f k8s/

# 5. Access
minikube service todo-frontend
```

## 📁 Files Structure

```
k8s/
├── backend-deployment.yaml
├── frontend-deployment.yaml
└── ingress.yaml
```

## 🌐 Access Application

```bash
# Method 1: Auto-open browser
minikube service todo-frontend

# Method 2: Get URL
minikube service todo-frontend --url

# Method 3: Port forward
kubectl port-forward service/todo-frontend 3000:3000
```

## 📊 Management Commands

```bash
# View resources
kubectl get pods
kubectl get services
kubectl get deployments

# View logs
kubectl logs -l app=todo-backend -f

# Scale
kubectl scale deployment todo-backend --replicas=3

# Update
kubectl rollout restart deployment/todo-backend
```

## 🐛 Troubleshooting

```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Restart Minikube
minikube stop
minikube start
```

## 🧹 Cleanup

```bash
kubectl delete -f k8s/
minikube stop
minikube delete
```

## ✅ Quick Reference

```bash
minikube start              # Start
minikube status             # Status
minikube dashboard          # Dashboard
kubectl get all             # View all
kubectl apply -f k8s/       # Deploy
kubectl delete -f k8s/      # Remove
```
