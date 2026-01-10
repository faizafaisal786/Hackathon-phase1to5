# Frontend Helm Chart

Helm chart for deploying the Todo Application Frontend web application.

## Features

- Next.js/React frontend deployment
- Service exposure
- Ingress configuration
- Horizontal Pod Autoscaling (HPA) support
- Health checks (liveness and readiness probes)
- Security context configuration
- Resource limits and requests
- Rolling update strategy

## Prerequisites

- Kubernetes 1.20+
- Helm 3.0+
- Ingress controller (if using ingress)

## Installation

```bash
# Install the frontend chart
helm install frontend ./frontend -n todo --create-namespace

# With custom values
helm install frontend ./frontend -f custom-values.yaml -n todo
```

## Configuration

### Basic Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Docker image repository | `hackathon-todo-frontend` |
| `image.tag` | Docker image tag | `latest` |
| `image.pullPolicy` | Pull policy | `IfNotPresent` |

### Service Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `3000` |

### Environment Variables

| Parameter | Description | Default |
|-----------|-------------|---------|
| `env.backendUrl` | Backend API URL | `http://backend:8000` |
| `env.apiBaseUrl` | API base path | `/api` |
| `env.environment` | Environment name | `production` |

### Ingress Configuration

```yaml
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: todo.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: todo-tls
      hosts:
        - todo.example.com
```

### Resource Configuration

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 300m
    memory: 256Mi
```

### Autoscaling

Enable HPA:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 80
```

## Examples

### Basic Deployment

```bash
helm install frontend ./frontend \
  -n todo \
  --create-namespace
```

### With Ingress

```bash
helm install frontend ./frontend \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=todo.example.com \
  --set ingress.className=nginx \
  -n todo \
  --create-namespace
```

### With TLS Certificate

```bash
helm install frontend ./frontend \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=todo.example.com \
  --set ingress.tls[0].secretName=todo-tls \
  --set ingress.tls[0].hosts[0]=todo.example.com \
  --set ingress.annotations."cert-manager\.io/cluster-issuer"=letsencrypt-prod \
  -n todo \
  --create-namespace
```

### Production Deployment

```bash
helm install frontend ./frontend \
  --set replicaCount=3 \
  --set autoscaling.enabled=true \
  --set autoscaling.maxReplicas=10 \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=todo.example.com \
  --set env.backendUrl=https://api.todo.example.com \
  -n todo-prod \
  --create-namespace
```

## Port Forwarding

For local development without ingress:

```bash
kubectl port-forward -n todo svc/frontend 3000:3000
```

Then visit: `http://localhost:3000`

## Environment Configuration

### Development

```bash
helm install frontend ./frontend \
  --set env.backendUrl=http://localhost:8000 \
  --set env.environment=development \
  -n todo-dev \
  --create-namespace
```

### Staging

```bash
helm install frontend ./frontend \
  --set env.backendUrl=https://api-staging.todo.example.com \
  --set env.environment=staging \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=staging.todo.example.com \
  -n todo-staging \
  --create-namespace
```

### Production

```bash
helm install frontend ./frontend \
  --set env.backendUrl=https://api.todo.example.com \
  --set env.environment=production \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=todo.example.com \
  --set replicaCount=3 \
  -n todo \
  --create-namespace
```

## Probes Configuration

### Liveness Probe

Checks if the pod is alive.

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Readiness Probe

Checks if the pod is ready to receive traffic.

```yaml
readinessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Security

The chart includes security best practices:

- Non-root user (UID 1000)
- Dropped capabilities
- No privilege escalation

## Upgrading

```bash
helm upgrade frontend ./frontend -n todo
```

## Uninstalling

```bash
helm uninstall frontend -n todo
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n todo -l app=frontend
kubectl describe pod <pod-name> -n todo
```

### View Logs

```bash
kubectl logs -n todo -l app=frontend
```

### Check Service

```bash
kubectl get svc -n todo frontend
kubectl describe svc frontend -n todo
```

### Check Ingress

```bash
kubectl get ingress -n todo
kubectl describe ingress frontend -n todo
```

## License

MIT
