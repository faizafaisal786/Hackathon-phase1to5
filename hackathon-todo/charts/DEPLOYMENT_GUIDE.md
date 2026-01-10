# Helm Chart Deployment Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Environments](#environments)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Usage](#advanced-usage)

## Quick Start

### Prerequisites
- Kubernetes cluster (1.20+)
- Helm 3.0+
- kubectl configured to access your cluster

### Installation Script
```bash
cd charts
chmod +x deploy.sh

# Development deployment
./deploy.sh -e dev

# Production deployment with OpenAI key
./deploy.sh -e prod -k $OPENAI_API_KEY

# Custom namespace and environment
./deploy.sh -e staging -n my-namespace -r my-release
```

### Manual Installation
```bash
cd charts

# Update dependencies
helm dependency update

# Install
helm install todo-app . -n todo --create-namespace

# Verify
kubectl get all -n todo
```

## Installation

### 1. Verify Prerequisites

```bash
# Check Kubernetes cluster
kubectl cluster-info
kubectl get nodes

# Check Helm version
helm version
```

### 2. Prepare Kubernetes Cluster

```bash
# Create namespace
kubectl create namespace todo

# Optional: Label nodes (for node affinity)
kubectl label nodes <node-name> workload=api
kubectl label nodes <node-name> workload=web
```

### 3. Update Dependencies

```bash
cd charts
helm dependency update
```

### 4. Install the Chart

```bash
# Basic installation
helm install todo-app . -n todo

# With custom values
helm install todo-app . -f values-prod.yaml -n todo

# With environment variables
helm install todo-app . \
  -n todo \
  --set backend.env.openaiApiKey=$OPENAI_API_KEY \
  --set frontend.env.backendUrl=https://api.example.com
```

## Configuration

### Environment-Specific Values

The chart includes pre-configured values files for different environments:

- **Development**: `values-dev.yaml`
  - 1 replica per service
  - Minimal resources
  - No ingress
  - Debug logging

- **Staging**: `values-staging.yaml`
  - 2 replicas per service
  - Moderate resources
  - Ingress enabled with staging domain
  - HPA enabled (2-4 replicas)

- **Production**: `values-prod.yaml`
  - 3 replicas per service
  - Full resources
  - Ingress with TLS
  - HPA enabled (3-10 replicas)
  - Pod anti-affinity
  - Node affinity

### Custom Configuration

Override any value:

```bash
helm install todo-app . \
  -n todo \
  --set backend.replicaCount=5 \
  --set frontend.replicaCount=5 \
  --set backend.resources.requests.cpu=1000m \
  --set frontend.resources.limits.memory=512Mi
```

### Secrets Management

The backend requires an OpenAI API key:

```bash
# Using --set
helm install todo-app . \
  -n todo \
  --set backend.env.openaiApiKey=$OPENAI_API_KEY

# Using a secret
kubectl create secret generic openai-secret \
  -n todo \
  --from-literal=api-key=$OPENAI_API_KEY

# Reference in values.yaml
backend:
  secrets:
    create: true
    openaiApiKey: ""  # Leave empty to create from secret
```

## Environments

### Development

```bash
# Deploy
helm install todo-app . -f values-dev.yaml -n todo-dev --create-namespace

# Access via port-forward
kubectl port-forward -n todo-dev svc/frontend 3000:3000
kubectl port-forward -n todo-dev svc/backend 8000:8000

# Visit
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/docs
```

### Staging

```bash
# Deploy with staging domain
helm install todo-app . \
  -f values-staging.yaml \
  -n todo-staging \
  --create-namespace \
  --set frontend.ingress.hosts[0].host=staging-todo.example.com

# Verify ingress
kubectl get ingress -n todo-staging

# Visit
# https://staging-todo.example.com
```

### Production

```bash
# Deploy with production settings
helm install todo-app . \
  -f values-prod.yaml \
  -n todo \
  --create-namespace \
  --set backend.env.openaiApiKey=$OPENAI_API_KEY \
  --set frontend.ingress.hosts[0].host=todo.example.com \
  --set frontend.env.backendUrl=https://api.todo.example.com

# Verify
kubectl get all -n todo
kubectl get ingress -n todo

# Visit
# https://todo.example.com
```

## Upgrading

### Update Values

```bash
# Upgrade with new values
helm upgrade todo-app . -f values-prod.yaml -n todo

# Upgrade specific values
helm upgrade todo-app . \
  -n todo \
  --set backend.replicaCount=5 \
  --set frontend.replicaCount=5
```

### Rolling Update Strategy

The charts use a rolling update strategy (maxSurge: 1, maxUnavailable: 0) for zero-downtime deployments.

```bash
# Monitor the rolling update
kubectl rollout status deployment/backend -n todo
kubectl rollout status deployment/frontend -n todo

# Check history
helm history todo-app -n todo

# Rollback if needed
helm rollback todo-app 1 -n todo
```

## Monitoring

### Pod Status

```bash
# All pods
kubectl get pods -n todo

# Detailed information
kubectl describe pod <pod-name> -n todo

# Real-time pod status
kubectl get pods -n todo -w
```

### Logs

```bash
# Backend logs
kubectl logs -n todo -l app=backend --tail=100

# Frontend logs
kubectl logs -n todo -l app=frontend --tail=100

# Real-time logs
kubectl logs -n todo -l app=backend -f
```

### Resource Usage

```bash
# Pod resource usage
kubectl top pods -n todo

# Node resource usage
kubectl top nodes

# Horizontal Pod Autoscaler status
kubectl get hpa -n todo
kubectl describe hpa backend -n todo
```

## Troubleshooting

### Common Issues

#### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n todo

# Check events
kubectl get events -n todo --sort-by='.lastTimestamp'

# Check logs
kubectl logs <pod-name> -n todo

# Common causes:
# - Image not found: Check image.repository and image.tag
# - Insufficient resources: Check node capacity
# - Missing secrets: Check secret configuration
```

#### Service Not Accessible

```bash
# Check service
kubectl get svc -n todo
kubectl describe svc backend -n todo

# Test service connectivity
kubectl run -it --rm debug --image=curlimages/curl:latest -n todo -- \
  curl http://backend:8000/health
```

#### Ingress Not Working

```bash
# Check ingress
kubectl get ingress -n todo
kubectl describe ingress frontend -n todo

# Check ingress controller
kubectl get pods -n ingress-nginx

# Verify DNS resolution
nslookup todo.example.com

# Test ingress from pod
kubectl run -it --rm debug --image=curlimages/curl:latest -n todo -- \
  curl -H "Host: todo.example.com" http://ingress-ip
```

#### High Memory/CPU Usage

```bash
# Check resource usage
kubectl top pods -n todo

# Adjust resource limits in values.yaml
backend:
  resources:
    limits:
      cpu: 500m
      memory: 512Mi

# Reapply
helm upgrade todo-app . -n todo
```

## Advanced Usage

### Custom Image Registry

```bash
helm install todo-app . \
  -n todo \
  --set backend.image.repository=my-registry.com/backend \
  --set frontend.image.repository=my-registry.com/frontend \
  --set backend.image.pullPolicy=Always \
  --set frontend.image.pullPolicy=Always
```

### Private Image Registry with Authentication

```bash
# Create image pull secret
kubectl create secret docker-registry regcred \
  --docker-server=my-registry.com \
  --docker-username=username \
  --docker-password=password \
  -n todo

# Reference in values.yaml
backend:
  imagePullSecrets:
    - name: regcred
```

### Database Integration

```bash
# Set database connection string
helm install todo-app . \
  -n todo \
  --set backend.env.databaseUrl=postgresql://user:pass@db-host:5432/todo
```

### TLS/SSL Configuration

```bash
# Using cert-manager with Let's Encrypt
helm install todo-app . \
  -n todo \
  -f values-prod.yaml \
  --set frontend.ingress.annotations."cert-manager\.io/cluster-issuer"=letsencrypt-prod \
  --set frontend.ingress.tls[0].secretName=todo-tls \
  --set frontend.ingress.tls[0].hosts[0]=todo.example.com
```

### Pod Disruption Budget

Add to values.yaml for production:

```yaml
podDisruptionBudget:
  enabled: true
  minAvailable: 1
```

### Network Policies

Restrict traffic between services:

```bash
# Backend can be accessed by frontend only
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-access
  namespace: todo
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8000
EOF
```

## Uninstalling

```bash
# Uninstall the release
helm uninstall todo-app -n todo

# Delete namespace
kubectl delete namespace todo
```

## Support and Issues

For issues or questions:
1. Check the troubleshooting section
2. Review logs: `kubectl logs -n todo -l app=backend`
3. Check events: `kubectl get events -n todo`
4. Verify configuration: `helm get values todo-app -n todo`

## License

MIT
