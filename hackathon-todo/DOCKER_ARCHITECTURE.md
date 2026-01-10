# Docker Deployment Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Host Machine                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │           Docker Compose Network                         ││
│  │           (hackathon-network: bridge)                    ││
│  ├─────────────────────────────────────────────────────────┤│
│  │                                                           ││
│  │  ┌──────────────────────┐  ┌───────────────────────┐   ││
│  │  │    Frontend (3000)   │  │   Backend (8000)      │   ││
│  │  ├──────────────────────┤  ├───────────────────────┤   ││
│  │  │ Next.js 14           │  │ FastAPI + Gunicorn    │   ││
│  │  │ • Build: alpine      │  │ • Python 3.11-slim    │   ││
│  │  │ • Port: 3000         │  │ • 4 workers           │   ││
│  │  │ • User: nextjs       │  │ • Port: 8000          │   ││
│  │  │ • Health: ✓ 30s      │  │ • Health: ✓ 30s       │   ││
│  │  │ • Size: ~200MB       │  │ • Size: ~250MB        │   ││
│  │  └──────────────────────┘  └───────────────────────┘   ││
│  │           ↓                       ↓                      ││
│  │           │◄──────────────────────┤                      ││
│  │           └──────────────────────→│                      ││
│  │                                   │                      ││
│  │                                   ↓                      ││
│  │                    ┌──────────────────────┐              ││
│  │                    │   Database (5432)    │              ││
│  │                    ├──────────────────────┤              ││
│  │                    │ PostgreSQL 15 Alpine │              ││
│  │                    │ • Port: 5432         │              ││
│  │                    │ • Health: ✓ 10s      │              ││
│  │                    │ • Volume: postgres   │              ││
│  │                    │ • Size: ~200MB       │              ││
│  │                    └──────────────────────┘              ││
│  │                                                           ││
│  └─────────────────────────────────────────────────────────┘│
│          ↑                                    ↑              │
│          │ localhost:3000                    │              │
│          │ (Frontend Access)                 │              │
│          │                    localhost:8000 │              │
│          │                    (API Access)   │              │
│          │                                    │              │
│  ┌───────┴────────────────────────────────────┴──────┐      │
│  │        Host Machine (Your Computer)               │      │
│  └───────────────────────────────────────────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Service Dependencies

```
              docker-compose up -d
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
      DB              Backend         Frontend
    (Postgres)      (FastAPI)       (Next.js)
   Status: ✓        Status: ✓       Status: ✓
        │              ▲              │
        └──────────────┤              │
                       │              │
                  waiting for      depends_on
                   DB Health      Backend Health
                       │              │
                       └──────────────┘
                            │
                       All Ready ✓
                    Ready for Traffic
```

## 🔄 Data Flow

### User Request Flow
```
1. User visits http://localhost:3000
   │
   ├─→ Frontend Container (Next.js)
   │   ├─ Serves React UI
   │   └─ Makes API calls to http://backend:8000
   │
   ├─→ Backend Container (FastAPI)
   │   ├─ Processes requests
   │   ├─ Calls OpenAI API
   │   ├─ Executes database queries
   │   └─ Returns JSON response
   │
   ├─→ Database Container (PostgreSQL)
   │   ├─ Stores/retrieves data
   │   └─ Persists conversations
   │
   └─→ Response returned to Frontend UI
```

### Conversation Save Flow
```
User Types Message
      │
      ▼
Frontend Component
      │
      ├─ POST /chat/
      ▼
Backend FastAPI
      │
      ├─ Create/Update Conversation in DB
      ├─ Save User Message
      ├─ Call AI Agent
      ├─ Save Assistant Message
      ▼
PostgreSQL
      │
      ├─ INSERT Conversation
      ├─ INSERT Messages
      ▼
Return Response with Conversation ID
      │
      ▼
Frontend Updates UI
      │
      ▼
Display Messages
```

## 📦 Image Composition

### Backend Image (`python:3.11-slim`)
```
Layer 1: Base OS (Debian slim)           [~50MB]
Layer 2: Python 3.11 Runtime             [~100MB]
Layer 3: System Dependencies (curl)      [~5MB]
Layer 4: Python Packages (copied)        [~50MB]
  ├─ FastAPI
  ├─ SQLModel
  ├─ Uvicorn
  ├─ Gunicorn
  ├─ OpenAI SDK
  └─ Other deps
Layer 5: Application Code                [~2MB]
──────────────────────────────────────────────────
Total Size: ~250MB (production ready)
```

### Frontend Image (`node:18-alpine`)
```
Layer 1: Alpine Linux Base               [~50MB]
Layer 2: Node.js 18 Runtime              [~100MB]
Layer 3: dumb-init & wget                [~5MB]
Layer 4: Production Dependencies         [~15MB]
  ├─ Next.js
  ├─ React
  ├─ Axios
  └─ Other deps
Layer 5: Next.js Build Output            [~30MB]
──────────────────────────────────────────────────
Total Size: ~200MB (production optimized)
```

## 🔌 Network Connectivity

### Internal Network (Docker)
```
Frontend              Backend              Database
(nextjs:3000) ←→ (fastapi:8000) ←→ (postgres:5432)

Service Names Resolve via DNS:
- frontend → 172.x.x.x:3000
- backend  → 172.x.x.y:8000
- db       → 172.x.x.z:5432
```

### External Network (Host)
```
Browser               Docker Host          Services
 │                      │                    │
 ├─→ localhost:3000 ──→ 127.0.0.1:3000 ─→ frontend:3000
 │
 ├─→ localhost:8000 ──→ 127.0.0.1:8000 ─→ backend:8000
 │
 └─→ localhost:5432 ──→ 127.0.0.1:5432 ─→ db:5432
```

## 📋 File Structure

```
hackathon-todo/
├── docker-compose.yml           ← Orchestration
├── .env.example                 ← Configuration template
│
├── app/                         ← Backend
│   ├── Dockerfile              ← Multi-stage, Gunicorn
│   ├── .dockerignore
│   ├── main.py
│   ├── models.py
│   ├── routers/
│   └── requirements.txt         ← Python dependencies
│
├── frontend/                    ← Frontend
│   ├── Dockerfile              ← Multi-stage, Alpine
│   ├── .dockerignore
│   ├── package.json            ← Node dependencies
│   ├── package-lock.json
│   ├── next.config.js
│   ├── tsconfig.json
│   └── src/
│
├── DOCKER_SETUP.md             ← Complete guide
├── DOCKER_COMMANDS.md          ← Command reference
├── DOCKERFILE_REFERENCE.md     ← Technical details
└── DOCKER_COMPLETE.md          ← Implementation summary
```

## 🚀 Deployment Checklist

- [x] Create Dockerfile for FastAPI backend
- [x] Create Dockerfile for Next.js frontend
- [x] Create docker-compose.yml with 3 services
- [x] Add .dockerignore files
- [x] Update requirements.txt with Gunicorn
- [x] Configure health checks
- [x] Set up environment variables
- [x] Add persistence with volumes
- [x] Create comprehensive documentation
- [x] Add command reference
- [x] Create architecture diagrams

## 🏃 Getting Started

### One-Time Setup
```bash
cd hackathon-todo
cp .env.example .env
# Edit .env and add OPENAI_API_KEY
```

### Start Application
```bash
docker-compose up -d
docker-compose ps           # Verify all running
```

### Access Services
```
Frontend:    http://localhost:3000
API:         http://localhost:8000
API Docs:    http://localhost:8000/docs
Database:    localhost:5432 (psql/postgres)
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Stop Application
```bash
docker-compose down          # Keep data
docker-compose down -v       # Remove everything
```

## 🔐 Security Features

✅ Multi-stage builds (reduced attack surface)
✅ Non-root user (frontend)
✅ Environment variable configuration
✅ Network isolation
✅ Health checks (auto-healing)
✅ Minimal base images

## ⚡ Performance Features

✅ Gunicorn + Uvicorn (4 workers)
✅ Alpine base images
✅ Slim Python image
✅ Optimized caching layers
✅ Production-ready configuration
✅ Resource limits ready

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| DOCKER_SETUP.md | Complete setup and configuration guide |
| DOCKER_COMMANDS.md | Quick reference for Docker commands |
| DOCKERFILE_REFERENCE.md | Technical details of Dockerfiles |
| DOCKER_COMPLETE.md | Implementation summary |

---

**Status**: ✅ **COMPLETE** - Production-ready Docker setup implemented
