#!/bin/bash
# Setup script for DigitalOcean Kubernetes cluster
# Usage: ./scripts/setup-cluster.sh

set -e

echo "============================================"
echo "DigitalOcean Kubernetes Cluster Setup"
echo "============================================"

# Check prerequisites
command -v doctl >/dev/null 2>&1 || { echo "doctl is required. Install: brew install doctl"; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "kubectl is required. Install: brew install kubectl"; exit 1; }
command -v helm >/dev/null 2>&1 || { echo "helm is required. Install: brew install helm"; exit 1; }

# Variables
CLUSTER_NAME="${CLUSTER_NAME:-hackathon-todo-k8s}"
NAMESPACE="${NAMESPACE:-hackathon-todo}"

echo ""
echo "Step 1: Configuring kubectl for cluster: $CLUSTER_NAME"
doctl kubernetes cluster kubeconfig save $CLUSTER_NAME

echo ""
echo "Step 2: Installing NGINX Ingress Controller..."
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm upgrade --install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.publishService.enabled=true \
  --wait

echo ""
echo "Step 3: Installing cert-manager..."
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm upgrade --install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true \
  --wait

echo ""
echo "Step 4: Installing Dapr..."
if ! command -v dapr &> /dev/null; then
    echo "Installing Dapr CLI..."
    wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
fi
dapr init -k --wait || echo "Dapr already installed"

echo ""
echo "Step 5: Creating namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "Step 6: Verifying installation..."
echo ""
echo "Nodes:"
kubectl get nodes
echo ""
echo "Dapr Status:"
dapr status -k
echo ""
echo "Ingress Controller:"
kubectl get svc -n ingress-nginx

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Get Load Balancer IP: kubectl get svc -n ingress-nginx"
echo "2. Configure DNS to point to the Load Balancer IP"
echo "3. Add GitHub secrets for CI/CD"
echo "4. Push to main/develop to trigger deployment"
echo ""
