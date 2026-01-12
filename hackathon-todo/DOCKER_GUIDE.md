# 🐳 Docker Deployment Guide

Complete guide for building and running the Todo App with Docker.

## 📋 Prerequisites

- Docker Desktop installed
- Docker Compose installed
- At least 4GB RAM available
- 2GB free disk space

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Using Build Scripts

**Windows:**
```bash
DOCKER_BUILD.bat
docker-compose up -d
```

**Linux/Mac:**
```bash
./DOCKER_BUILD.sh
docker-compose up -d
```

### Option 3: Manual Build

```bash
# Build backend
docker build -t todo-backend -f backend/Dockerfile .

# Build frontend
docker build -t todo-frontend ./frontend

# Run with docker-compose
docker-compose up -d
```

## 🔧 Configuration

### Environment Variables

**Backend (.env or docker-compose.yml):**
```env
OPENAI_API_KEY=demo           # Use "demo" for FREE mode
PYTHONUNBUFFERED=1            # Python logging
```

**Frontend:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=production
```

### Ports

- **3000**: Frontend (Next.js)
- **8000**: Backend (FastAPI)

To change ports, edit `docker-compose.yml`:
```yaml
ports:
  - "YOUR_PORT:3000"  # Frontend
  - "YOUR_PORT:8000"  # Backend
```

## 📁 Data Persistence

Data is stored in volumes:

```yaml
volumes:
  - ./backend/tasks.json:/app/tasks.json
  - ./backend/conversations.db:/app/conversations.db
```

This ensures your data persists across container restarts.

## 🛠️ Docker Commands

### Build Commands

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Build without cache
docker-compose build --no-cache
```

### Run Commands

```bash
# Start services in background
docker-compose up -d

# Start services in foreground
docker-compose up

# Start specific service
docker-compose up backend
```

### Stop Commands

```bash
# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove with volumes
docker-compose down -v
```

### Log Commands

```bash
# View all logs
docker-compose logs

# Follow logs
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Status Commands

```bash
# Check status
docker-compose ps

# View resource usage
docker stats
```

## 🔍 Debugging

### Check Container Health

```bash
# View health status
docker ps

# Inspect container
docker inspect todo-backend
docker inspect todo-frontend
```

### Access Container Shell

```bash
# Backend shell
docker exec -it todo-backend bash

# Frontend shell
docker exec -it todo-frontend sh
```

### View Application Logs

```bash
# Backend logs
docker logs todo-backend

# Frontend logs
docker logs todo-frontend

# Follow logs
docker logs -f todo-backend
```

## 🔄 Updates & Rebuilds

### After Code Changes

```bash
# Rebuild and restart
docker-compose up -d --build

# Or rebuild specific service
docker-compose build backend
docker-compose up -d backend
```

### Clean Rebuild

```bash
# Stop everything
docker-compose down

# Remove images
docker rmi todo-backend todo-frontend

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

## 📊 Resource Management

### View Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df
```

### Clean Up

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove all unused data
docker system prune -a
```

## 🌐 Production Deployment

### Build Production Images

```bash
# Tag images
docker tag todo-backend:latest your-registry/todo-backend:v1.0
docker tag todo-frontend:latest your-registry/todo-frontend:v1.0

# Push to registry
docker push your-registry/todo-backend:v1.0
docker push your-registry/todo-frontend:v1.0
```

### Docker Hub Deployment

```bash
# Login
docker login

# Tag
docker tag todo-backend your-username/todo-backend:latest
docker tag todo-frontend your-username/todo-frontend:latest

# Push
docker push your-username/todo-backend:latest
docker push your-username/todo-frontend:latest
```

### Pull and Run on Server

```bash
# Pull images
docker pull your-username/todo-backend:latest
docker pull your-username/todo-frontend:latest

# Run with docker-compose
docker-compose up -d
```

## 🔐 Security Best Practices

1. **Use Non-Root User**
   - Frontend runs as user `nextjs` (UID 1001)
   - Backend runs with minimal privileges

2. **Environment Variables**
   - Never commit .env files
   - Use Docker secrets in production
   - Rotate API keys regularly

3. **Network Isolation**
   - Services communicate via Docker network
   - Only expose necessary ports

4. **Resource Limits**
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '1'
             memory: 512M
   ```

## 📝 Troubleshooting

### Common Issues

**Issue: Port already in use**
```bash
# Find process using port
netstat -ano | findstr :3000  # Windows
lsof -i :3000                 # Linux/Mac

# Kill process or change port in docker-compose.yml
```

**Issue: Build fails**
```bash
# Clear Docker cache
docker builder prune -a

# Rebuild without cache
docker-compose build --no-cache
```

**Issue: Container keeps restarting**
```bash
# Check logs
docker logs todo-backend

# Check health
docker inspect todo-backend | grep Health -A 10
```

**Issue: Cannot connect to backend from frontend**
```bash
# Check network
docker network inspect todo-network

# Verify backend is running
curl http://localhost:8000
```

## 📈 Performance Optimization

### Multi-Stage Builds

Already implemented in Dockerfiles:
- Frontend: base → deps → builder → runner
- Backend: Single optimized stage

### Caching

```dockerfile
# Copy dependencies first (better caching)
COPY package.json package-lock.json ./
RUN npm install

# Then copy code
COPY . .
```

### Image Size

```bash
# View image sizes
docker images

# Optimize by:
# - Using alpine base images
# - Multi-stage builds
# - Removing dev dependencies
```

## 🧪 Testing Docker Build

```bash
# Test build
docker-compose build

# Test run
docker-compose up -d

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/api/tasks
curl http://localhost:3000

# Check health
docker ps

# Stop
docker-compose down
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Next.js Docker Documentation](https://nextjs.org/docs/deployment#docker-image)
- [FastAPI Docker Documentation](https://fastapi.tiangolo.com/deployment/docker/)

## 🎯 Summary

**Quick Commands:**

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

✅ **Docker setup complete! Your app is containerized and ready to deploy!**
