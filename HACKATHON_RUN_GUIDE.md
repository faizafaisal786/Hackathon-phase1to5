# 🚀 Hackathon - Har Phase Run Karne Ka Tareeqa

## Phase 1: Python CLI App (todo-phase1)

### Kya Hai?
Simple command-line task manager (in-memory storage)

### Kaise Run Karein?
```bash
cd todo-phase1
python src/main.py
```

### Kya Milega?
- Menu-based interface
- Add, List, Update, Delete, Mark Complete tasks
- Data memory mein rahega (exit karne par delete)

---

## Phase 2: Backend + Frontend (hackathon-todo)

### Kya Hai?
Full-stack web application with FastAPI backend aur Next.js frontend

### Backend Run Karne Ka Tareeqa:

#### Quick Start (Recommended):
```bash
cd hackathon-todo
python run.py
```

Backend chal jayega: http://localhost:8000

#### Ya phir Direct Start:
```bash
cd hackathon-todo
uvicorn app.main:app --reload
```

### Frontend Run Karne Ka Tareeqa:
```bash
cd hackathon-todo/frontend
npm install
npm run dev
```

Frontend chal jayega: http://localhost:3000

### Dono Ek Saath Chalane Ke Liye:
**Terminal 1:**
```bash
cd hackathon-todo
python run.py
```

**Terminal 2:**
```bash
cd hackathon-todo/frontend
npm run dev
```

---

## Phase 3: Backend + AI Chat (hackathon-todo with AI)

### Kya Hai?
Backend with AI chatbot integration (FREE demo mode)

### Kaise Run Karein?
```bash
cd hackathon-todo
python run.py
```

### AI Chat Test Karna:
1. Browser mein jaao: http://localhost:8000/docs
2. `/chat` endpoint try karo
3. Example message: "Add a task to buy groceries"

### Features:
- Natural language task management
- FREE demo mode (no API key needed)
- OpenAI integration ready (optional)

---

## Phase 4: Docker + Kubernetes (helm-chart-project)

### Kya Hai?
Containerized application with Kubernetes deployment

### Prerequisites:
- Docker Desktop installed
- Kubernetes enabled (Docker Desktop settings)

### Docker Se Run Karna:

#### Backend Container:
```bash
cd hackathon-todo
docker build -f Dockerfile.backend-simple -t todo-backend .
docker run -p 8000:8000 todo-backend
```

#### Frontend Container:
```bash
cd hackathon-todo
docker build -f Dockerfile.frontend-simple -t todo-frontend .
docker run -p 3000:3000 todo-frontend
```

#### Docker Compose Se Dono Ek Saath:
```bash
cd hackathon-todo
docker-compose up
```

### Kubernetes/Helm Se Run Karna:
```bash
cd helm-chart-project
helm install todo-app ./charts/todo-app
```

Check status:
```bash
kubectl get pods
kubectl get services
```

---

## 📋 Quick Reference Table

| Phase | Technology | Run Command | Port |
|-------|-----------|-------------|------|
| Phase 1 | Python CLI | `python src/main.py` | - |
| Phase 2 (Backend) | FastAPI | `python run.py` | 8000 |
| Phase 2 (Frontend) | Next.js | `npm run dev` | 3000 |
| Phase 3 | FastAPI + AI | `python run.py` | 8000 |
| Phase 4 | Docker | `docker-compose up` | 8000, 3000 |
| Phase 4 | Kubernetes | `helm install todo-app ./charts/todo-app` | K8s managed |

---

## 🔍 Troubleshooting

### Port already in use?
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Virtual environment activate nahi ho raha?
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Docker running nahi hai?
```bash
docker --version
docker ps
# Docker Desktop kholo aur start karo
```

### Kubernetes cluster nahi chal raha?
```bash
# Docker Desktop settings -> Enable Kubernetes
kubectl cluster-info
```

---

## ✅ Testing URLs

### Phase 2 & 3:
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

### Phase 4 (Docker):
- Same as Phase 2 & 3

### Phase 4 (Kubernetes):
```bash
kubectl get services
# Use the external IP or NodePort
```

---

## 🎯 Recommended Flow

1. **Phase 1**: Pehle CLI app run karo aur samjho
2. **Phase 2**: Backend chalao, phir frontend add karo
3. **Phase 3**: AI chat feature test karo
4. **Phase 4**: Docker se containerize karo, phir K8s deploy karo

---

**Happy Coding! 🚀**
