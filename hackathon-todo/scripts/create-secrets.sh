#!/bin/bash
# Create Kubernetes secrets for the application
# Usage: ./scripts/create-secrets.sh

set -e

# Check for required environment variables
: "${REDPANDA_BROKERS:?Environment variable REDPANDA_BROKERS is required}"
: "${REDPANDA_USERNAME:?Environment variable REDPANDA_USERNAME is required}"
: "${REDPANDA_PASSWORD:?Environment variable REDPANDA_PASSWORD is required}"
: "${DIGITALOCEAN_TOKEN:?Environment variable DIGITALOCEAN_TOKEN is required}"

# Optional
OPENAI_API_KEY="${OPENAI_API_KEY:-demo}"
NAMESPACE="${NAMESPACE:-hackathon-todo}"

echo "Creating secrets in namespace: $NAMESPACE"

# Create namespace if not exists
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Redpanda credentials
echo "Creating Redpanda credentials..."
kubectl create secret generic redpanda-credentials \
  --namespace=$NAMESPACE \
  --from-literal=brokers="$REDPANDA_BROKERS" \
  --from-literal=username="$REDPANDA_USERNAME" \
  --from-literal=password="$REDPANDA_PASSWORD" \
  --dry-run=client -o yaml | kubectl apply -f -

# App secrets
echo "Creating app secrets..."
kubectl create secret generic app-secrets \
  --namespace=$NAMESPACE \
  --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
  --dry-run=client -o yaml | kubectl apply -f -

# Registry credentials
echo "Creating registry credentials..."
kubectl create secret docker-registry registry-credentials \
  --namespace=$NAMESPACE \
  --docker-server=registry.digitalocean.com \
  --docker-username="$DIGITALOCEAN_TOKEN" \
  --docker-password="$DIGITALOCEAN_TOKEN" \
  --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "All secrets created successfully!"
kubectl get secrets -n $NAMESPACE
