# 🚀 AI-Powered Todo App - Hackathon Edition

> **A revolutionary task management application with AI agent, MCP protocol, bilingual support, and 100% FREE operation!**

[![Status](https://img.shields.io/badge/status-production_ready-green)]() [![Docker](https://img.shields.io/badge/docker-ready-blue)]() [![Kubernetes](https://img.shields.io/badge/kubernetes-ready-blue)]() [![FREE](https://img.shields.io/badge/cost-FREE-brightgreen)]()

**Winner Features:** AI Chat Interface | FREE Demo Mode | MCP Protocol | Hindi/Hinglish Support | Cloud-Native Architecture

## ✨ Key Features

### 🏆 Hackathon Innovation Highlights

#### 🤖 AI-Powered Task Management
- **Chat with AI** - Natural language interface for task management
- **FREE Demo Mode** - No API key required! Works 100% offline
- **OpenAI Integration** - Optional GPT-4o-mini support
- **Smart Date Parsing** - "tomorrow", "kal", "next week" automatically understood

#### 🌏 Bilingual Natural Language Processing
- **English Support** - "Add a task to buy groceries tomorrow"
- **Hindi/Hinglish Support** - "Kal ka kaam add kar do"
- **Smart Command Detection** - Understands context and intent
- **Date Recognition** - Parses dates in both languages

#### 🔧 MCP Protocol Implementation
- **Model Context Protocol** - Industry-standard AI tool interface
- **5 Tool Functions** - add_task, list_tasks, complete_task, update_task, delete_task
- **Extensible Architecture** - Easy to add new capabilities
- **Future-Proof Design** - Compatible with any MCP-enabled AI

#### ☁️ Cloud-Native & Production Ready
- **Docker Containerized** - Build once, run anywhere
- **Kubernetes Manifests** - Auto-scaling with health checks
- **Minikube Deployment** - One-command local cluster setup
- **Multi-Stage Builds** - Optimized image sizes

### 🎯 Core Features
- **User Authentication**: Secure JWT-based auth with registration/login
- **Task CRUD Operations**: Full create, read, update, delete functionality
- **Real-time Chat**: Conversation history and context awareness
- **Task Filters**: View pending, completed, or all tasks
- **Modern UI**: Responsive design with Tailwind CSS
- **Type Safety**: Full TypeScript frontend, Python type hints backend
- **Health Monitoring**: Liveness and readiness probes
- **Auto-Scaling**: Kubernetes horizontal pod autoscaling support

## 💬 AI Chat Examples

### English Commands
```
You: "Add a task to buy groceries tomorrow"
AI: "I've added the task 'buy groceries' with due date 2026-01-13!"

You: "Show me all my tasks"
AI: "Here are your tasks:
     1. buy groceries (pending) - Due: 2026-01-13"

You: "Complete the first task"
AI: "Task 'buy groceries' marked as completed!"
```

### Hindi/Hinglish Commands
```
You: "Kal ka kaam add kar do - dentist appointment"
AI: "Maine 'dentist appointment' ka task kal ke liye add kar diya!"

You: "Sab tasks dikha do"
AI: "Aapke tasks:
     1. dentist appointment (pending) - Due: 2026-01-13"

You: "Pehla task complete kar"
AI: "Task 'dentist appointment' complete ho gaya!"
```

## 💻 Tech Stack

### Backend
- **FastAPI** - High-performance async Python web framework
- **Python 3.11** - Latest Python with enhanced performance
- **SQLModel** - SQL database ORM with Pydantic integration
- **MCP SDK** - Model Context Protocol implementation
- **OpenAI SDK** - GPT integration (optional, FREE mode available)
- **JWT Authentication** - Secure token-based auth
- **Uvicorn** - Lightning-fast ASGI server

### Frontend
- **Next.js 14** - React framework with App Router & SSR
- **TypeScript** - Type-safe JavaScript for reliability
- **React 18** - Latest React with concurrent features
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client with interceptors

### DevOps & Deployment
- **Docker** - Container platform
- **Docker Compose** - Multi-container orchestration
- **Kubernetes** - Production-grade orchestration
- **Minikube** - Local K8s testing
- **GitHub Actions Ready** - CI/CD pipeline support

## Project Structure

```
hackathon-todo/
├── app/                    # FastAPI backend
│   ├── routers/
│   │   ├── auth.py        # Authentication endpoints
│   │   └── tasks.py       # Task CRUD endpoints
│   ├── models.py          # SQLModel database models
│   ├── auth.py            # JWT utilities
│   ├── database.py        # Database connection
│   ├── dependencies.py    # FastAPI dependencies
│   ├── config.py          # Configuration settings
│   └── main.py            # Main FastAPI app
├── frontend/              # Next.js frontend
│   └── src/
│       ├── app/           # Next.js pages
│       ├── components/    # React components
│       ├── contexts/      # React contexts (Auth)
│       └── lib/           # API client
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## 🚀 Quick Start (3 Options)

### Option 1: Docker Compose (Recommended - 1 Command!)

```bash
cd hackathon-todo
docker-compose up -d
```

**Access immediately:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Features enabled:**
- ✅ FREE AI mode (no API key needed)
- ✅ All services running
- ✅ Data persistence
- ✅ Auto-restart on crash

### Option 2: Kubernetes/Minikube (Cloud-Native)

```bash
cd hackathon-todo
minikube start
./MINIKUBE_DEPLOY.sh  # Windows: MINIKUBE_DEPLOY.bat
minikube service todo-frontend
```

**What you get:**
- ✅ 2 backend replicas (auto-scaling)
- ✅ 2 frontend replicas (load balanced)
- ✅ Health checks & monitoring
- ✅ Production-ready setup

### Option 3: Local Development

**Backend:**
```bash
cd hackathon-todo
pip install -r requirements.txt
cd backend && python main.py
```

**Frontend (new terminal):**
```bash
cd hackathon-todo/frontend
npm install && npm run dev
```

## 📋 Prerequisites

**For Docker/Kubernetes:**
- Docker Desktop installed
- (Optional) Minikube for K8s deployment

**For Local Development:**
- Python 3.11+ installed
- Node.js 18+ installed
- No database needed (uses JSON file storage)

### Backend Setup

1. **Navigate to the project root**:
   ```bash
   cd hackathon-todo
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Neon database URL:
   ```env
   DATABASE_URL=postgresql://user:password@host/database
   SECRET_KEY=your-secret-key-here-change-this
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   APP_NAME=Hackathon Todo API
   DEBUG=True
   ```

5. **Run the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create a `.env.local` file:
   ```bash
   cp .env.local.example .env.local
   ```

   Edit `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "password",
    "full_name": "Full Name"
  }
  ```

- `POST /auth/login` - Login (form data)
- `POST /auth/token` - Login (JSON)
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```

### Tasks (All require JWT authentication)

- `GET /tasks` - List all tasks (optional `?completed=true/false`)
- `POST /tasks` - Create a new task
  ```json
  {
    "title": "Task title",
    "description": "Task description",
    "completed": false
  }
  ```
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/complete` - Mark task as complete
- `PATCH /tasks/{id}/incomplete` - Mark task as incomplete

## Authentication Flow

1. User registers or logs in via `/auth/register` or `/auth/token`
2. Backend returns a JWT access token
3. Frontend stores the token in localStorage
4. Token is included in all subsequent API requests via `Authorization: Bearer <token>` header
5. Backend validates the token on protected routes

## Database Schema

### User Table
- `id` (Primary Key)
- `email` (Unique)
- `username` (Unique)
- `full_name` (Optional)
- `hashed_password`
- `is_active`
- `created_at`

### Task Table
- `id` (Primary Key)
- `title`
- `description` (Optional)
- `completed` (Boolean)
- `owner_id` (Foreign Key to User)
- `created_at`
- `updated_at`

## Development

### Running Tests
```bash
# Backend tests (add pytest configuration)
pytest

# Frontend tests (add test framework)
npm test
```

### Building for Production

**Backend**:
```bash
# The FastAPI app can be deployed to any platform supporting Python
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run build
npm start
```

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT encoding
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `DEBUG`: Debug mode (True/False)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Protected API routes
- CORS configuration for frontend
- User ownership verification for tasks

## Deployment

### Backend Deployment Options
- **Railway**: Easy deployment with PostgreSQL
- **Render**: Free tier available
- **Heroku**: Classic PaaS option
- **DigitalOcean App Platform**: Managed deployment

### Frontend Deployment Options
- **Vercel**: Optimized for Next.js
- **Netlify**: Static site hosting
- **Railway**: Full-stack deployment

### Neon Database
The app is configured to work with Neon's serverless PostgreSQL. Get your connection string from [neon.tech](https://neon.tech).

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

For issues and questions, please open an issue on the GitHub repository.
