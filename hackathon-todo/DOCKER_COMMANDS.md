# Docker Quick Reference

## Starting the Application

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## Stopping the Application

```bash
# Stop services (keep data)
docker-compose stop

# Stop and remove containers (keep volumes)
docker-compose down

# Stop and remove everything including volumes
docker-compose down -v
```

## Checking Status

```bash
# List running containers
docker-compose ps

# View service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Stream logs
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail 100 backend
```

## Development Commands

```bash
# Rebuild without cache
docker-compose build --no-cache

# Restart a specific service
docker-compose restart backend

# Stop a specific service
docker-compose stop frontend

# Start a specific service
docker-compose start frontend

# Run a one-off command
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec db psql -U postgres
```

## Useful Debugging Commands

```bash
# View container statistics
docker stats

# Inspect container details
docker inspect hackathon-backend

# Check container logs with timestamp
docker-compose logs --timestamps backend

# Execute command in container
docker-compose exec backend python -c "import app; print(app.__version__)"

# Check network connectivity between services
docker-compose exec backend ping db

# Database health check
docker-compose exec db pg_isready -U postgres
```

## Database Commands

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d hackathon_todo

# List databases
docker-compose exec db psql -U postgres -l

# Backup database
docker-compose exec db pg_dump -U postgres hackathon_todo > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres hackathon_todo < backup.sql

# Delete database
docker-compose exec db psql -U postgres -c "DROP DATABASE hackathon_todo;"

# Create database
docker-compose exec db psql -U postgres -c "CREATE DATABASE hackathon_todo;"
```

## Cleaning Up

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Clean everything (be careful!)
docker system prune -a
```

## Building and Publishing

```bash
# Build specific service
docker-compose build backend

# Build with specific tag
docker build -t hackathon-backend:v1.0 ./app

# Push to registry
docker push your-registry/hackathon-backend:v1.0

# Pull latest images
docker-compose pull
```

## Environment and Configuration

```bash
# View environment variables in container
docker-compose exec backend env

# Override environment variable for one-off command
docker-compose exec -e DEBUG=True backend bash

# Update .env file and restart services
nano .env
docker-compose up -d
```

## Performance and Resource Management

```bash
# Monitor container resource usage
docker stats hackathon-backend

# Limit container memory (temporary)
docker update --memory 512m hackathon-backend

# View image size
docker images | grep hackathon

# Check disk usage
docker system df

# Prune build cache
docker builder prune
```

## Accessing Services

```bash
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
# Alternative docs: http://localhost:8000/redoc

# Database connection
# Host: localhost
# Port: 5432
# User: postgres
# Password: postgres (default)
# Database: hackathon_todo
```

## Common Issues and Fixes

```bash
# Port already in use
# Change port in docker-compose.yml and rebuild

# Container exiting immediately
docker-compose logs backend

# Out of memory
docker system prune -a
docker-compose up -d

# Network issues
docker-compose down
docker network prune
docker-compose up -d

# Permission denied
sudo usermod -aG docker $USER
newgrp docker
```

## Advanced Commands

```bash
# View compose file with variables substituted
docker-compose config

# Validate compose file
docker-compose config --quiet

# Run services with specific profile
docker-compose --profile debug up

# Use different compose file
docker-compose -f docker-compose.dev.yml up

# Scale service (if supported)
docker-compose up --scale backend=2

# View build layers
docker history hackathon-backend:latest

# Diff container changes
docker diff hackathon-backend

# Export/Import images
docker save hackathon-backend > backend.tar
docker load < backend.tar
```

## Useful Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
alias dc='docker-compose'
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'
alias dclogs='docker-compose logs -f'
alias dcexec='docker-compose exec'
alias dcps='docker-compose ps'
alias dcbuild='docker-compose build'
alias dcrestart='docker-compose restart'
```

Then use:
```bash
dc ps
dcup
dclogs backend
```

## Monitoring and Health

```bash
# Check service health
docker-compose ps

# View health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Restart unhealthy containers automatically
# Already configured in docker-compose.yml with restart: unless-stopped

# Manual health check
docker-compose exec backend curl http://localhost:8000/health
docker-compose exec frontend wget -O- http://localhost:3000
```
