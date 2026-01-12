#!/bin/bash

echo "================================================"
echo "  Building Docker Images"
echo "================================================"
echo ""

cd "$(dirname "$0")"

echo "[1/3] Building Backend Image..."
docker build -t todo-backend -f backend/Dockerfile .
if [ $? -ne 0 ]; then
    echo "ERROR: Backend build failed"
    exit 1
fi
echo "Backend image built successfully!"
echo ""

echo "[2/3] Building Frontend Image..."
docker build -t todo-frontend ./frontend
if [ $? -ne 0 ]; then
    echo "ERROR: Frontend build failed"
    exit 1
fi
echo "Frontend image built successfully!"
echo ""

echo "[3/3] Images Built Successfully!"
echo ""
echo "================================================"
echo "  Docker Images Ready:"
echo "  - todo-backend"
echo "  - todo-frontend"
echo ""
echo "  To run the containers:"
echo "  docker-compose up -d"
echo "================================================"
echo ""
