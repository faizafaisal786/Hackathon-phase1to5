# Todo Application Helm Chart

This is the root Helm chart for the Todo Application, which includes both frontend and backend services as subcharts.

## Prerequisites

- Kubernetes 1.20+
- Helm 3.0+
- kubectl configured to connect to your cluster

## Quick Start

### 1. Install the Chart

```bash
# Navigate to the charts directory
cd charts

# Update dependencies
helm dependency update

# Install the chart
helm install todo-app . --namespace todo --create-namespace
```

### 2. Access Your Application

For the frontend:
```bash
kubectl port-forward -n todo svc/frontend 3000:3000
# Visit http://localhost:3000
```

For the backend API:
```bash
kubectl port-forward -n todo svc/backend 8000:8000
# Visit http://localhost:8000/docs (FastAPI Swagger UI)
```

## Configuration

### Global Configuration

The root `values.yaml` file controls both subcharts:

```bash
# Install with custom values
helm install todo-app . -f custom-values.yaml --namespace todo
```

### Backend Configuration

Override backend settings:

```bash
helm install todo-app . \
  --set backend.replicaCount=3 \
  --set backend.resources.requests.cpu=500m \
  --set backend.env.openaiApiKey=$OPENAI_API_KEY \
  --namespace todo
```

### Frontend Configuration

Override frontend settings:

```bash
helm install todo-app . \
  --set frontend.ingress.enabled=true \
  --set frontend.ingress.hosts[0].host=myapp.example.com \
  --namespace todo
```

### Enable Ingress

To expose your frontend through an ingress controller:

```bash
helm install todo-app . \
  --set frontend.ingress.enabled=true \
  --set frontend.ingress.className=nginx \
  --set frontend.ingress.hosts[0].host=todo.example.com \
  --namespace todo
```

### Enable Autoscaling

Enable Horizontal Pod Autoscaling:

```bash
helm install todo-app . \
  --set backend.autoscaling.enabled=true \
  --set backend.autoscaling.minReplicas=2 \
  --set backend.autoscaling.maxReplicas=5 \
  --set frontend.autoscaling.enabled=true \
  --namespace todo
```

## Upgrading

```bash
helm upgrade todo-app . --namespace todo
```

## Uninstalling

```bash
helm uninstall todo-app --namespace todo
```

## Values Reference

### Backend Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.enabled` | Enable backend deployment | `true` |
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.image.repository` | Backend image repository | `hackathon-todo-backend` |
| `backend.image.tag` | Backend image tag | `latest` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.env.openaiApiKey` | OpenAI API key | `` |
| `backend.resources.requests.cpu` | Backend CPU request | `250m` |
| `backend.resources.requests.memory` | Backend memory request | `256Mi` |

### Frontend Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.enabled` | Enable frontend deployment | `true` |
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.image.repository` | Frontend image repository | `hackathon-todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `latest` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.ingress.enabled` | Enable ingress | `true` |
| `frontend.ingress.hosts[0].host` | Ingress host | `todo.example.com` |

## Examples

### Production Setup

```bash
helm install todo-app . \
  --set backend.replicaCount=3 \
  --set backend.autoscaling.enabled=true \
  --set backend.autoscaling.maxReplicas=5 \
  --set backend.env.openaiApiKey=$OPENAI_API_KEY \
  --set frontend.replicaCount=3 \
  --set frontend.autoscaling.enabled=true \
  --set frontend.autoscaling.maxReplicas=5 \
  --set frontend.ingress.enabled=true \
  --set frontend.ingress.hosts[0].host=todo.example.com \
  --set frontend.ingress.className=nginx \
  --namespace todo \
  --create-namespace
```

### Development Setup

```bash
helm install todo-app . \
  --set backend.replicaCount=1 \
  --set backend.resources.requests.cpu=100m \
  --set frontend.replicaCount=1 \
  --set frontend.resources.requests.cpu=50m \
  --set frontend.ingress.enabled=false \
  --namespace todo-dev \
  --create-namespace
```

### Staging with TLS

```bash
helm install todo-app . \
  --set backend.replicaCount=2 \
  --set frontend.replicaCount=2 \
  --set frontend.ingress.enabled=true \
  --set frontend.ingress.hosts[0].host=staging.todo.example.com \
  --set frontend.ingress.tls[0].secretName=staging-tls \
  --set frontend.ingress.tls[0].hosts[0]=staging.todo.example.com \
  --namespace todo-staging \
  --create-namespace
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n todo
kubectl describe pod <pod-name> -n todo
```

### View Logs

```bash
# Backend logs
kubectl logs -n todo -l app=backend --tail=100

# Frontend logs
kubectl logs -n todo -l app=frontend --tail=100
```

### Debug Issues

```bash
# Check services
kubectl get svc -n todo

# Check deployments
kubectl get deployments -n todo

# Describe deployment
kubectl describe deployment backend -n todo
```

## Environment Variables

### Backend

- `OPENAI_API_KEY`: OpenAI API key for AI features
- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: Application environment (production, staging, development)
- `LOG_LEVEL`: Logging level (debug, info, warning, error)

### Frontend

- `BACKEND_URL`: Backend API URL
- `API_BASE_URL`: API base path
- `ENVIRONMENT`: Application environment

## License

MIT
