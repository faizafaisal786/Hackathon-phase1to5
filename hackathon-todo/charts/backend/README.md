# Backend Helm Chart

Helm chart for deploying the Todo Application Backend API service.

## Features

- FastAPI backend deployment
- ConfigMap and Secret management
- Service exposure
- Horizontal Pod Autoscaling (HPA) support
- Health checks (liveness and readiness probes)
- Security context configuration
- Resource limits and requests
- Rolling update strategy

## Prerequisites

- Kubernetes 1.20+
- Helm 3.0+

## Installation

```bash
# Install the backend chart
helm install backend ./backend -n todo --create-namespace

# With custom values
helm install backend ./backend -f custom-values.yaml -n todo
```

## Configuration

### Basic Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Docker image repository | `hackathon-todo-backend` |
| `image.tag` | Docker image tag | `latest` |
| `image.pullPolicy` | Pull policy | `IfNotPresent` |

### Service Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `8000` |

### Environment Variables

| Parameter | Description | Default |
|-----------|-------------|---------|
| `env.openaiApiKey` | OpenAI API key | `` |
| `env.databaseUrl` | Database connection URL | `` |
| `env.environment` | Environment name | `production` |
| `env.logLevel` | Log level | `info` |

### Resource Configuration

```yaml
resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

### Autoscaling

Enable HPA:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80
```

## Examples

### Development Deployment

```bash
helm install backend ./backend \
  --set replicaCount=1 \
  --set resources.requests.cpu=100m \
  -n todo-dev \
  --create-namespace
```

### Production Deployment with HPA

```bash
helm install backend ./backend \
  --set replicaCount=2 \
  --set autoscaling.enabled=true \
  --set autoscaling.maxReplicas=10 \
  --set env.openaiApiKey=$OPENAI_API_KEY \
  --set env.databaseUrl=$DB_URL \
  -n todo-prod \
  --create-namespace
```

## Probes Configuration

### Liveness Probe

Checks if the pod is alive and should be restarted if failing.

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Readiness Probe

Checks if the pod is ready to receive traffic.

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Security

The chart includes security best practices:

- Non-root user (UID 1000)
- Read-only root filesystem (can be disabled)
- Dropped capabilities
- No privilege escalation

## Upgrading

```bash
helm upgrade backend ./backend -n todo
```

## Uninstalling

```bash
helm uninstall backend -n todo
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n todo -l app=backend
kubectl describe pod <pod-name> -n todo
```

### View Logs

```bash
kubectl logs -n todo -l app=backend
```

### Check Service

```bash
kubectl get svc -n todo backend
kubectl describe svc backend -n todo
```

## Health Endpoints

The backend exposes:
- `/health` - Health check endpoint
- `/docs` - Swagger UI documentation
- `/redoc` - ReDoc documentation

## License

MIT
