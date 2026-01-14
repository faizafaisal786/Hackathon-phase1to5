# Cloud Deployment Guide

Complete guide to deploy the Hackathon Todo app on DigitalOcean Kubernetes (DOKS) with Redpanda Cloud and GitHub Actions CI/CD.

## Prerequisites

- GitHub account (free)
- DigitalOcean account ($200 free credit for new users)
- Redpanda Cloud account (free tier available)
- Domain name (optional, can use DigitalOcean load balancer IP)

---

## 1. DigitalOcean Setup

### 1.1 Create DOKS Cluster

1. Go to [DigitalOcean Kubernetes](https://cloud.digitalocean.com/kubernetes)
2. Click **Create Kubernetes Cluster**
3. Configure:
   - **Region:** Choose closest to your users
   - **Version:** Latest stable (1.28+)
   - **Node Pool:**
     - **Node Plan:** Basic ($12/month per node)
     - **Nodes:** 2 (minimum for HA)
   - **Name:** `hackathon-todo-k8s`
4. Click **Create Cluster** (~5 minutes)

**Estimated Cost:** $24/month (2 basic nodes)

### 1.2 Create Container Registry

1. Go to [Container Registry](https://cloud.digitalocean.com/registry)
2. Click **Create Registry**
3. Configure:
   - **Name:** `hackathon-todo`
   - **Plan:** Starter (free, 500MB)
4. Click **Create Registry**

### 1.3 Generate API Token

1. Go to [API Tokens](https://cloud.digitalocean.com/account/api/tokens)
2. Click **Generate New Token**
3. Configure:
   - **Name:** `github-actions-deploy`
   - **Expiration:** No expiry
   - **Scopes:** Read & Write
4. **Copy the token immediately** (shown only once)

### 1.4 Install doctl CLI

```bash
# macOS
brew install doctl

# Windows
scoop install doctl

# Linux
snap install doctl

# Authenticate
doctl auth init
# Paste your API token when prompted
```

### 1.5 Configure kubectl

```bash
# Download cluster config
doctl kubernetes cluster kubeconfig save hackathon-todo-k8s

# Verify connection
kubectl get nodes
```

---

## 2. Redpanda Cloud Setup (Free Tier)

### 2.1 Create Account

1. Go to [Redpanda Cloud](https://cloud.redpanda.com)
2. Sign up with GitHub/Google (free)
3. Choose **Serverless** tier (free)

### 2.2 Create Cluster

1. Click **Create Cluster**
2. Configure:
   - **Type:** Serverless (free tier)
   - **Region:** Choose same as DOKS cluster
   - **Name:** `hackathon-todo`
3. Click **Create**

### 2.3 Get Connection Details

After cluster is created:

1. Go to **Overview** tab
2. Copy **Bootstrap Server URL** (e.g., `seed-xxx.redpanda.com:9092`)
3. Go to **Security** → **SASL Users**
4. Click **Create User**:
   - **Username:** `hackathon-todo`
   - **Password:** Generate or set your own
   - **Mechanism:** SCRAM-SHA-256
5. Copy credentials

### 2.4 Create Topics

1. Go to **Topics** tab
2. Create topics:

| Topic Name | Partitions | Retention |
|------------|------------|-----------|
| `task-events` | 3 | 7 days |
| `reminder-events` | 2 | 1 day |
| `notification-events` | 2 | 1 day |
| `dead-letter-queue` | 1 | 30 days |

---

## 3. Install Cluster Components

### 3.1 Install NGINX Ingress Controller

```bash
# Add Helm repo
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.publishService.enabled=true
```

### 3.2 Install cert-manager (for SSL)

```bash
# Add Helm repo
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true
```

### 3.3 Install Dapr

```bash
# Install Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Initialize Dapr on cluster
dapr init -k --wait

# Verify installation
dapr status -k
```

---

## 4. GitHub Repository Setup

### 4.1 Fork/Clone Repository

```bash
git clone https://github.com/your-username/hackathon-todo.git
cd hackathon-todo
```

### 4.2 Configure GitHub Secrets

Go to **Repository Settings** → **Secrets and variables** → **Actions**

Add the following secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `DIGITALOCEAN_ACCESS_TOKEN` | `dop_v1_xxx...` | DO API token |
| `REDPANDA_BROKERS` | `seed-xxx.redpanda.com:9092` | Redpanda bootstrap server |
| `REDPANDA_USERNAME` | `hackathon-todo` | SASL username |
| `REDPANDA_PASSWORD` | `your-password` | SASL password |
| `OPENAI_API_KEY` | `sk-xxx...` | OpenAI API key (optional) |

### 4.3 Configure Environments

1. Go to **Settings** → **Environments**
2. Create `staging` environment
3. Create `production` environment with:
   - **Required reviewers:** Add yourself
   - **Wait timer:** 5 minutes (optional)

---

## 5. Deploy Application

### 5.1 Manual First Deployment

```bash
# Create namespace
kubectl create namespace hackathon-todo

# Create secrets manually first time
kubectl create secret generic redpanda-credentials \
  --namespace=hackathon-todo \
  --from-literal=brokers="YOUR_REDPANDA_BROKERS" \
  --from-literal=username="YOUR_USERNAME" \
  --from-literal=password="YOUR_PASSWORD"

kubectl create secret generic app-secrets \
  --namespace=hackathon-todo \
  --from-literal=OPENAI_API_KEY="YOUR_OPENAI_KEY"

# Create registry secret
kubectl create secret docker-registry registry-credentials \
  --namespace=hackathon-todo \
  --docker-server=registry.digitalocean.com \
  --docker-username="YOUR_DO_TOKEN" \
  --docker-password="YOUR_DO_TOKEN"

# Build and push images
doctl registry login

docker build -t registry.digitalocean.com/hackathon-todo/backend:v1 ./hackathon-todo/backend
docker push registry.digitalocean.com/hackathon-todo/backend:v1

docker build -t registry.digitalocean.com/hackathon-todo/frontend:v1 ./hackathon-todo/frontend
docker push registry.digitalocean.com/hackathon-todo/frontend:v1

docker build -t registry.digitalocean.com/hackathon-todo/reminder-service:v1 ./hackathon-todo/reminder-service
docker push registry.digitalocean.com/hackathon-todo/reminder-service:v1

# Deploy with Kustomize
cd hackathon-todo/k8s/overlays/production
kustomize edit set image \
  registry.digitalocean.com/hackathon-todo/backend:v1 \
  registry.digitalocean.com/hackathon-todo/frontend:v1 \
  registry.digitalocean.com/hackathon-todo/reminder-service:v1
kustomize build . | kubectl apply -f -
```

### 5.2 Automated Deployment (GitHub Actions)

After initial setup, deployments are automatic:

- **Push to `develop`** → Deploy to Staging
- **Push to `main`** → Deploy to Production
- **Create tag `v*`** → Deploy to Production + Create Release

---

## 6. Domain Configuration

### 6.1 Get Load Balancer IP

```bash
kubectl get svc -n ingress-nginx
# Note the EXTERNAL-IP of nginx-ingress-controller
```

### 6.2 Configure DNS

Add A records pointing to the Load Balancer IP:

| Type | Name | Value |
|------|------|-------|
| A | @ | `<LOAD_BALANCER_IP>` |
| A | api | `<LOAD_BALANCER_IP>` |
| A | staging | `<LOAD_BALANCER_IP>` |
| A | api-staging | `<LOAD_BALANCER_IP>` |

### 6.3 Update Ingress (if using custom domain)

Edit `k8s/base/ingress.yaml` with your domain:

```yaml
spec:
  rules:
    - host: your-domain.com
    - host: api.your-domain.com
```

---

## 7. Monitoring & Debugging

### 7.1 View Logs

```bash
# All pods
kubectl logs -f -l app.kubernetes.io/part-of=hackathon-todo -n hackathon-todo

# Specific service
kubectl logs -f deployment/backend -n hackathon-todo
kubectl logs -f deployment/reminder-service -n hackathon-todo

# Dapr sidecar
kubectl logs -f deployment/backend -c daprd -n hackathon-todo
```

### 7.2 Check Pod Status

```bash
kubectl get pods -n hackathon-todo
kubectl describe pod <pod-name> -n hackathon-todo
```

### 7.3 Check Dapr Components

```bash
dapr components -k -n hackathon-todo
dapr configurations -k -n hackathon-todo
```

### 7.4 Test Pub/Sub

```bash
# Port forward to backend
kubectl port-forward svc/backend 8000:80 -n hackathon-todo

# Create a task (triggers event)
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "due_date": "2024-12-31", "reminder_before": 60}'
```

---

## 8. Cost Summary (Free/Low Cost)

| Service | Cost | Notes |
|---------|------|-------|
| DigitalOcean DOKS | $24/month | 2 basic nodes |
| DigitalOcean Registry | Free | Starter tier (500MB) |
| Redpanda Cloud | Free | Serverless tier |
| GitHub Actions | Free | 2000 min/month |
| Let's Encrypt SSL | Free | via cert-manager |
| **Total** | **~$24/month** | New users get $200 credit |

---

## 9. Troubleshooting

### Pods not starting

```bash
kubectl describe pod <pod-name> -n hackathon-todo
kubectl logs <pod-name> -n hackathon-todo --previous
```

### Dapr sidecar issues

```bash
kubectl logs <pod-name> -c daprd -n hackathon-todo
dapr dashboard -k
```

### Image pull errors

```bash
# Verify registry credentials
kubectl get secret registry-credentials -n hackathon-todo -o yaml

# Re-create if needed
kubectl delete secret registry-credentials -n hackathon-todo
# Then recreate with correct token
```

### Redpanda connection issues

```bash
# Test from a pod
kubectl run -it --rm debug --image=alpine --restart=Never -- sh
apk add kafkacat
kafkacat -b YOUR_BROKERS -L -X security.protocol=SASL_SSL -X sasl.mechanisms=SCRAM-SHA-256 -X sasl.username=USER -X sasl.password=PASS
```

---

## 10. Scaling

### Horizontal Pod Autoscaler

```bash
kubectl autoscale deployment backend -n hackathon-todo \
  --min=2 --max=10 --cpu-percent=70

kubectl autoscale deployment frontend -n hackathon-todo \
  --min=2 --max=10 --cpu-percent=70
```

### Add More Nodes

```bash
doctl kubernetes cluster node-pool update hackathon-todo-k8s <pool-id> \
  --count 3
```

---

## Quick Reference

```bash
# Deploy to staging
git push origin develop

# Deploy to production
git push origin main

# Create release
git tag v1.0.0
git push origin v1.0.0

# Manual rollback
kubectl rollout undo deployment/backend -n hackathon-todo

# View all resources
kubectl get all -n hackathon-todo
```
