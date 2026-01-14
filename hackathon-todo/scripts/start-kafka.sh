#!/bin/bash

# Start Kafka infrastructure with Docker Compose
# Usage: ./scripts/start-kafka.sh

set -e

echo "=========================================="
echo "Starting Kafka Event-Driven Infrastructure"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo ""
echo "Building and starting services..."
echo ""

# Start infrastructure first
docker-compose -f docker-compose.kafka.yml up -d zookeeper redis

echo "Waiting for Zookeeper and Redis..."
sleep 5

# Start Kafka
docker-compose -f docker-compose.kafka.yml up -d kafka

echo "Waiting for Kafka to be ready..."
sleep 10

# Initialize Kafka topics
docker-compose -f docker-compose.kafka.yml up kafka-init

# Start application services
echo ""
echo "Starting application services..."
docker-compose -f docker-compose.kafka.yml up -d backend backend-dapr reminder-service reminder-dapr

echo ""
echo "Waiting for services to initialize..."
sleep 10

# Start frontend
docker-compose -f docker-compose.kafka.yml up -d frontend

# Start Kafka UI (optional monitoring)
docker-compose -f docker-compose.kafka.yml up -d kafka-ui

echo ""
echo "=========================================="
echo "Services Started Successfully!"
echo "=========================================="
echo ""
echo "Available endpoints:"
echo "  - Frontend:        http://localhost:3000"
echo "  - Backend API:     http://localhost:8000"
echo "  - Reminder Service: http://localhost:8001"
echo "  - Kafka UI:        http://localhost:8080"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker-compose.kafka.yml logs -f"
echo ""
echo "To stop all services:"
echo "  docker-compose -f docker-compose.kafka.yml down"
echo ""
