# Dockerfile Summary

## Backend Dockerfile (`app/Dockerfile`)

### Multi-Stage Build
- **Stage 1 (Builder)**: Installs all dependencies including build tools
- **Stage 2 (Runtime)**: Copies only production packages, reducing final size

### Key Features
```dockerfile
# Python 3.11 slim base image (~145MB)
FROM python:3.11-slim as builder
FROM python:3.11-slim

# Build-time dependencies: gcc, g++, make (removed in runtime)
# Runtime dependencies: curl (for health checks)

# Health check: Monitors /health endpoint every 30s
# Restart policy: Auto-restart on failure

# Production server: Gunicorn + Uvicorn workers (4 workers)
```

### Image Details
- **Base Image**: python:3.11-slim
- **Final Size**: ~250MB (with all dependencies)
- **Working Directory**: /app
- **Entry Point**: gunicorn with uvicorn workers
- **Health Check**: Every 30 seconds to /health endpoint
- **Exposed Port**: 8000

### Build Command
```bash
docker build -t hackathon-backend:latest ./app
```

### Run Command
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-xxx \
  -e SECRET_KEY=secret \
  hackathon-backend:latest
```

---

## Frontend Dockerfile (`frontend/Dockerfile`)

### Multi-Stage Build
- **Stage 1 (Builder)**: Builds Next.js application with dev dependencies
- **Stage 2 (Production)**: Serves built app with only production dependencies

### Key Features
```dockerfile
# Node.js 18 alpine base image (~150MB)
FROM node:18-alpine as builder
FROM node:18-alpine

# Build-time: Next.js compiler, TypeScript, build tools
# Runtime: dumb-init (signal handling), wget (health checks)

# Non-root user: nextjs (uid: 1001) for security
# Health check: Monitors root URL every 30s
# Proper signal handling: dumb-init as entrypoint
```

### Image Details
- **Base Image**: node:18-alpine
- **Final Size**: ~200MB (with production dependencies)
- **Working Directory**: /app
- **Non-Root User**: nextjs (1001:1001)
- **Entry Point**: dumb-init (proper signal handling)
- **Health Check**: Every 30 seconds to root URL
- **Exposed Port**: 3000

### Build Command
```bash
docker build -t hackathon-frontend:latest ./frontend
```

### Run Command
```bash
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  hackathon-frontend:latest
```

---

## .dockerignore Files

### Backend `.dockerignore` (`app/.dockerignore`)
Excludes unnecessary files:
- Python cache files (__pycache__, *.pyc)
- Virtual environments
- Git files
- Tests and coverage
- IDE files

### Frontend `.dockerignore` (`frontend/.dockerignore`)
Excludes unnecessary files:
- Node modules (rebuild in container)
- Build artifacts
- Git files
- IDE files
- Cache files

---

## Size Optimization

### Backend Image Layers
```
Layer 1: python:3.11-slim (145MB)
Layer 2: System packages (20MB)
Layer 3: Builder dependencies (80MB) [discarded]
Layer 4: Python packages (50MB) [copied from builder]
Layer 5: Application code (2MB)
────────────────────────────────
Total: ~250MB
```

### Frontend Image Layers
```
Layer 1: node:18-alpine (150MB)
Layer 2: Build dependencies (40MB) [discarded]
Layer 3: Node packages build (60MB) [discarded]
Layer 4: Next.js build output (30MB)
Layer 5: Production dependencies (15MB)
Layer 6: Application code (5MB)
────────────────────────────────
Total: ~200MB
```

---

## Production Deployment

### Backend - Production Settings
```dockerfile
# Server: Gunicorn with Uvicorn workers
CMD ["gunicorn", 
     "app.main:app", 
     "--workers", "4",                    # 4 concurrent workers
     "--worker-class", "uvicorn.workers.UvicornWorker",
     "--bind", "0.0.0.0:8000"]

# Health checks every 30s with 3 retries
# Auto-restart on failure
# Read-only filesystem support available
```

### Frontend - Production Settings
```dockerfile
# Non-root user for security
USER nextjs (1001:1001)

# dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]

# Next.js production server
CMD ["npm", "start"]

# Health checks every 30s with 3 retries
```

---

## Docker Compose Integration

### Service Configuration
```yaml
backend:
  build:
    context: .
    dockerfile: app/Dockerfile
  container_name: hackathon-backend
  ports: ["8000:8000"]
  healthcheck: 
    test: curl -f http://localhost:8000/health
    interval: 30s, timeout: 10s, retries: 3

frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  container_name: hackathon-frontend
  ports: ["3000:3000"]
  depends_on:
    backend: { condition: service_healthy }
```

### Network Communication
- Services communicate by name within Docker network
- Backend accessible as: `http://backend:8000`
- Database accessible as: `postgresql://db:5432`

---

## Environment Variables

### Backend
```
OPENAI_API_KEY        # Required: OpenAI API key
SECRET_KEY            # Required: JWT signing key
DATABASE_URL          # Optional: Database connection (default: SQLite)
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

### Frontend
```
NEXT_PUBLIC_API_URL   # Backend API URL (default: http://localhost:8000)
NODE_ENV              # Environment: development|production
```

---

## Security Considerations

### Implemented ✅
- Multi-stage builds (smaller attack surface)
- Non-root user execution (frontend)
- Environment variable configuration
- Health checks (auto-healing)
- Resource limits available

### Additional Recommendations
- Use secrets management (Docker Secrets)
- Read-only root filesystem
- Network policies
- Regular image scanning
- Version pinning
- Signed images

---

## Performance Tuning

### Backend
```
Workers: 4 (set based on CPU cores)
Worker timeout: 120s (default)
Keep-alive: 5s (default)
Max requests per worker: Unlimited
```

Adjust with environment variables or command line arguments.

### Frontend
```
Node heap size: 512MB (default)
Production optimizations: Enabled
Image optimization: Enabled
Static generation: At build time
```

---

## Troubleshooting

### Image Build Issues
```bash
# Verbose build output
docker build --progress=plain -t app:latest .

# Check layers
docker history app:latest

# Inspect build cache
docker builder du
```

### Container Runtime Issues
```bash
# Check logs
docker logs hackathon-backend

# Inspect container
docker inspect hackathon-backend

# View processes
docker top hackathon-backend

# Check network
docker network inspect hackathon-network
```

### Performance Issues
```bash
# Monitor resources
docker stats hackathon-backend

# Check disk usage
docker system df

# Review image layers
docker history --no-trunc app:latest
```

---

## Maintenance

### Regular Tasks
```bash
# Scan for vulnerabilities
docker scan hackathon-backend

# Update base images
docker pull python:3.11-slim
docker pull node:18-alpine

# Rebuild images
docker-compose build --pull

# Cleanup
docker system prune -a
```

### Backup and Recovery
```bash
# Save image
docker save hackathon-backend:latest | gzip > backend.tar.gz

# Load image
docker load < backend.tar.gz

# Export database
docker-compose exec db pg_dump -U postgres > backup.sql

# Import database
docker-compose exec -T db psql -U postgres < backup.sql
```

---

## References

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Python Docker Best Practices](https://github.com/docker-library/python/blob/main/README.md)
- [Node.js Docker Best Practices](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
