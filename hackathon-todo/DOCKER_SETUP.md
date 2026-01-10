# Docker Setup Guide

## Overview
This project uses Docker and Docker Compose to containerize both the FastAPI backend and Next.js frontend applications, along with a PostgreSQL database.

## Architecture

```
┌─────────────────────────────────────────────────┐
│          Docker Compose Network                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │  Next.js         │  │  FastAPI         │   │
│  │  Frontend        │──│  Backend         │   │
│  │  (Port 3000)     │  │  (Port 8000)     │   │
│  └──────────────────┘  └──────────────────┘   │
│                               │                │
│                               ▼                │
│                        ┌──────────────────┐   │
│                        │  PostgreSQL DB   │   │
│                        │  (Port 5432)     │   │
│                        └──────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Services

### 1. Backend Service (FastAPI)
- **Image**: Python 3.11-slim with multi-stage build
- **Port**: 8000
- **Features**:
  - Gunicorn with Uvicorn workers for production
  - Health checks enabled
  - Volume mounting for live development
  - Environment variable configuration

**Dockerfile**: `app/Dockerfile`
- Multi-stage build to reduce image size
- Separates build and runtime dependencies
- Non-root user execution (recommended)
- Health check: `/health` endpoint

### 2. Frontend Service (Next.js)
- **Image**: Node.js 18-alpine with multi-stage build
- **Port**: 3000
- **Features**:
  - Optimized production build
  - Non-root user execution
  - Health checks enabled
  - Environment variables for API URL configuration

**Dockerfile**: `frontend/Dockerfile`
- Multi-stage build (build → production)
- Only production dependencies in final image
- Dumb-init for proper signal handling
- Health check via HTTP request

### 3. Database Service (PostgreSQL)
- **Image**: PostgreSQL 15-alpine
- **Port**: 5432
- **Features**:
  - Persistent volume for data
  - Health checks enabled
  - Configurable via environment variables

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- `.env` file with required variables (see below)

### 1. Create `.env` file
```bash
# Create .env file in project root
OPENAI_API_KEY=sk-your-openai-api-key
SECRET_KEY=your-super-secret-key-change-in-production
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=hackathon_todo
```

### 2. Build and Start Services
```bash
# Build images
docker-compose build

# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Access Applications
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432 (postgres/postgres)

## Commands

### View Status
```bash
# List running containers
docker-compose ps

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Real-time logs
docker-compose logs -f backend
```

### Development
```bash
# Build with no cache
docker-compose build --no-cache

# Start services
docker-compose up

# Stop services (without removing)
docker-compose stop

# Restart services
docker-compose restart

# Remove all containers and volumes
docker-compose down -v
```

### Debugging
```bash
# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh

# View container logs
docker-compose logs backend --tail 100

# Check container stats
docker stats

# Inspect container
docker inspect hackathon-backend
```

## Docker Images

### Backend Image Details
- **Base Image**: `python:3.11-slim`
- **Size**: ~150MB (optimized with multi-stage build)
- **Entry Point**: Gunicorn with Uvicorn workers
- **Workers**: 4 workers for concurrent requests
- **Health Check**: HTTP GET to `/health` endpoint

**Image Layers**:
1. Python base image
2. Build dependencies
3. Python packages
4. Runtime dependencies only
5. Application code

### Frontend Image Details
- **Base Image**: `node:18-alpine`
- **Size**: ~200MB (optimized with multi-stage build)
- **Entry Point**: npm start
- **Process Manager**: dumb-init (proper signal handling)
- **User**: Non-root `nextjs` user (uid: 1001)
- **Health Check**: HTTP GET to application root

**Image Layers**:
1. Node.js base image
2. Build dependencies
3. Node packages and build
4. Next.js build output
5. Production dependencies only

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=sk-...           # OpenAI API key
SECRET_KEY=secret-key           # JWT secret key
ALGORITHM=HS256                 # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30  # Token expiration
DATABASE_URL=sqlite:///./data/todo.db  # DB connection string
```

### Frontend (.env)
```
NEXT_PUBLIC_API_URL=http://backend:8000  # Backend API URL (inside Docker)
NODE_ENV=production                       # Environment
```

## Networking

### Network Configuration
- **Network Name**: `hackathon-network`
- **Driver**: bridge
- **DNS**: Service names resolvable within network
  - `backend:8000` - FastAPI backend
  - `db:5432` - PostgreSQL database

### Service Communication
- Frontend can access backend at: `http://backend:8000`
- Backend can access database at: `db:5432`
- External access via localhost ports

## Volumes

### Persistent Storage
```
volumes:
  postgres_data:      # PostgreSQL data persistence
  backend_data:       # Backend application data
```

### Volume Mounting
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect hackathon-todo_postgres_data

# Clean up unused volumes
docker volume prune
```

## Health Checks

Each service includes health checks:

### Backend Health Check
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

### Frontend Health Check
```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

### Database Health Check
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 10s
  timeout: 5s
  retries: 5
```

## Security Best Practices

### Implemented
✅ Non-root user execution (frontend)
✅ Multi-stage builds to reduce attack surface
✅ Environment variable configuration
✅ .dockerignore for sensitive files
✅ Health checks for auto-restart

### Recommended for Production
- Use Docker secrets for sensitive data
- Implement read-only root filesystem
- Set resource limits (memory, CPU)
- Use private registry for images
- Enable Docker content trust
- Regular image vulnerability scanning
- Use version tags instead of latest

### Example Production Configuration
```yaml
services:
  backend:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp
```

## Performance Optimization

### Backend
- Gunicorn with 4 workers (configurable)
- Multi-stage build reduces image size
- Slim base image reduces resource usage
- Connection pooling via SQLModel

### Frontend
- Next.js production build optimizations
- Alpine Linux reduces image size
- Only production dependencies
- Dumb-init reduces memory overhead

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs backend

# Inspect container
docker inspect hackathon-backend

# Rebuild without cache
docker-compose build --no-cache
```

### Port Already in Use
```bash
# Find process using port
lsof -i :8000
netstat -an | grep 8000

# Change port in docker-compose.yml
# ports:
#   - "8001:8000"
```

### Database Connection Issues
```bash
# Check database is running
docker-compose exec db psql -U postgres -c "SELECT 1"

# Check network connectivity
docker-compose exec backend ping db

# View database logs
docker-compose logs db
```

### Memory Issues
```bash
# Check memory usage
docker stats

# Reduce worker count for backend
# In app/Dockerfile: --workers 2

# Limit service memory
# In docker-compose.yml: deploy.resources.limits.memory
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Docker Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          push: false
          tags: hackathon-app:latest
```

## Deployment

### Kubernetes
Services can be easily converted to Kubernetes manifests using tools like Kompose.

### Docker Swarm
Services can be deployed to Docker Swarm in production mode.

### Cloud Platforms
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

## Maintenance

### Regular Tasks
```bash
# Clean up unused resources
docker system prune -a

# Update images
docker-compose pull
docker-compose build --pull

# Check for vulnerabilities
docker scan hackathon-backend
docker scan hackathon-frontend

# Backup database
docker-compose exec db pg_dump -U postgres hackathon_todo > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres hackathon_todo < backup.sql
```

## References
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/dev-best-practices/)
