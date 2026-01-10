#!/bin/bash

# Helm Chart Deployment Script for Todo Application
# This script helps deploy the Todo app to Kubernetes using Helm

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
NAMESPACE="todo"
ENVIRONMENT="dev"
RELEASE_NAME="todo-app"
CHARTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENAI_API_KEY=""

# Functions
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -e, --environment ENV          Environment: dev, staging, prod (default: dev)"
    echo "  -n, --namespace NAMESPACE      Kubernetes namespace (default: todo)"
    echo "  -r, --release RELEASE_NAME     Helm release name (default: todo-app)"
    echo "  -k, --openai-key KEY           OpenAI API key"
    echo "  -h, --help                     Show this help message"
    echo ""
    echo "Examples:"
    echo "  # Deploy to development"
    echo "  $0 -e dev"
    echo ""
    echo "  # Deploy to production with OpenAI key"
    echo "  $0 -e prod -k \$OPENAI_API_KEY"
    echo ""
    echo "  # Deploy to custom namespace"
    echo "  $0 -e staging -n my-namespace"
}

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -r|--release)
            RELEASE_NAME="$2"
            shift 2
            ;;
        -k|--openai-key)
            OPENAI_API_KEY="$2"
            shift 2
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
    print_error "Invalid environment: $ENVIRONMENT"
    exit 1
fi

print_info "Deploying Todo Application"
print_info "Environment: $ENVIRONMENT"
print_info "Namespace: $NAMESPACE"
print_info "Release Name: $RELEASE_NAME"
print_info "Charts Directory: $CHARTS_DIR"

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    print_error "Helm is not installed. Please install Helm first."
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Create namespace if it doesn't exist
print_info "Checking namespace..."
if ! kubectl get namespace "$NAMESPACE" &> /dev/null; then
    print_info "Creating namespace: $NAMESPACE"
    kubectl create namespace "$NAMESPACE"
else
    print_info "Namespace already exists: $NAMESPACE"
fi

# Update Helm dependencies
print_info "Updating Helm dependencies..."
cd "$CHARTS_DIR"
helm dependency update

# Prepare values file
VALUES_FILE="values-${ENVIRONMENT}.yaml"
if [[ ! -f "$VALUES_FILE" ]]; then
    print_error "Values file not found: $VALUES_FILE"
    exit 1
fi

print_info "Using values file: $VALUES_FILE"

# Build helm install command
HELM_INSTALL_CMD="helm install $RELEASE_NAME . --namespace $NAMESPACE -f $VALUES_FILE"

# Add OpenAI key if provided
if [[ -n "$OPENAI_API_KEY" ]]; then
    print_info "Using provided OpenAI API key"
    HELM_INSTALL_CMD="$HELM_INSTALL_CMD --set backend.env.openaiApiKey=$OPENAI_API_KEY"
fi

# Check if release already exists
if helm list -n "$NAMESPACE" | grep -q "$RELEASE_NAME"; then
    print_warn "Release already exists. Upgrading..."
    HELM_INSTALL_CMD="${HELM_INSTALL_CMD/install/upgrade}"
fi

# Deploy
print_info "Deploying Helm chart..."
eval "$HELM_INSTALL_CMD"

# Wait for deployment
print_info "Waiting for deployments to be ready..."
kubectl rollout status deployment -n "$NAMESPACE" -l app=backend --timeout=5m || true
kubectl rollout status deployment -n "$NAMESPACE" -l app=frontend --timeout=5m || true

# Print access information
print_info "Deployment complete!"
echo ""
echo -e "${GREEN}Access Information:${NC}"
echo ""

# Check if ingress is enabled
if helm get values "$RELEASE_NAME" -n "$NAMESPACE" | grep -q "ingress.*enabled.*true"; then
    print_info "Ingress is enabled"
    echo "Frontend Ingress:"
    kubectl get ingress -n "$NAMESPACE"
else
    print_info "Port forwarding required to access services"
    echo ""
    echo "Backend:"
    echo "  kubectl port-forward -n $NAMESPACE svc/backend 8000:8000"
    echo ""
    echo "Frontend:"
    echo "  kubectl port-forward -n $NAMESPACE svc/frontend 3000:3000"
fi

echo ""
echo -e "${GREEN}Useful Commands:${NC}"
echo "View deployment status:"
echo "  kubectl get pods -n $NAMESPACE"
echo ""
echo "View logs:"
echo "  kubectl logs -n $NAMESPACE -l app=backend"
echo "  kubectl logs -n $NAMESPACE -l app=frontend"
echo ""
echo "Upgrade deployment:"
echo "  helm upgrade $RELEASE_NAME . -n $NAMESPACE -f $VALUES_FILE"
echo ""
echo "Uninstall deployment:"
echo "  helm uninstall $RELEASE_NAME -n $NAMESPACE"
