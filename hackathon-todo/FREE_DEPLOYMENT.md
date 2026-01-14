# 100% FREE Cloud Deployment Guide

Deploy the complete system for **$0/month** using free tiers.

## Free Services Used

| Service | Free Tier | Usage |
|---------|-----------|-------|
| **Vercel** | Unlimited | Frontend hosting |
| **Railway** | $5/month credit | Backend + Reminder Service |
| **Upstash Redis** | 10K commands/day | State store |
| **Upstash Kafka** | 10K messages/day | Event streaming |
| **GitHub Actions** | 2000 min/month | CI/CD |

**Total Cost: $0/month**

---

## Step 1: Upstash Setup (5 minutes)

### 1.1 Create Upstash Account
1. Go to [upstash.com](https://upstash.com)
2. Sign up with GitHub (FREE)

### 1.2 Create Redis Database
1. Click **Create Database**
2. Select:
   - **Name:** `hackathon-todo-redis`
   - **Region:** Choose closest
   - **Type:** Regional (Free)
3. Copy connection details:
   - `UPSTASH_REDIS_URL`
   - `UPSTASH_REDIS_TOKEN`

### 1.3 Create Kafka Cluster
1. Go to **Kafka** tab
2. Click **Create Cluster**
3. Select:
   - **Name:** `hackathon-todo-kafka`
   - **Region:** Same as Redis
   - **Type:** Single Replica (Free)
4. Create Topics:
   - `task-events`
   - `reminder-events`
5. Copy connection details:
   - `UPSTASH_KAFKA_URL`
   - `UPSTASH_KAFKA_USERNAME`
   - `UPSTASH_KAFKA_PASSWORD`

---

## Step 2: Railway Setup (10 minutes)

### 2.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (FREE - $5 credit/month)

### 2.2 Deploy Backend
1. Click **New Project** → **Deploy from GitHub repo**
2. Select your repository
3. Configure:
   - **Root Directory:** `hackathon-todo/backend`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
```
OPENAI_API_KEY=your-key-or-demo
UPSTASH_REDIS_URL=your-redis-url
UPSTASH_KAFKA_BROKERS=your-kafka-url
UPSTASH_KAFKA_USERNAME=your-username
UPSTASH_KAFKA_PASSWORD=your-password
EVENTS_ENABLED=true
```
5. Deploy → Copy the URL (e.g., `backend-xxx.railway.app`)

### 2.3 Deploy Reminder Service
1. In same project, click **New Service** → **GitHub Repo**
2. Configure:
   - **Root Directory:** `hackathon-todo/reminder-service`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add same environment variables
4. Deploy

---

## Step 3: Vercel Setup (5 minutes)

### 3.1 Deploy Frontend
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub (FREE)
3. Click **Import Project** → Select repository
4. Configure:
   - **Root Directory:** `hackathon-todo/frontend`
   - **Framework:** Next.js (auto-detected)
5. Add Environment Variable:
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```
6. Deploy → Get URL (e.g., `hackathon-todo.vercel.app`)

---

## Step 4: Quick Setup Files

### vercel.json (Frontend)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

### railway.json (Backend)
```json
{
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "restartPolicyType": "on_failure"
  }
}
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    VERCEL (FREE)                             │
│                    Frontend (Next.js)                        │
│                    hackathon-todo.vercel.app                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAILWAY (FREE $5/mo)                      │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │  Backend API        │  │  Reminder Service   │          │
│  │  FastAPI + Events   │  │  Cron + Events      │          │
│  └──────────┬──────────┘  └──────────┬──────────┘          │
└─────────────┼────────────────────────┼──────────────────────┘
              │                        │
              ▼                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    UPSTASH (FREE)                            │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │  Kafka              │  │  Redis              │          │
│  │  (Event Streaming)  │  │  (State Store)      │          │
│  │  10K msgs/day       │  │  10K cmds/day       │          │
│  └─────────────────────┘  └─────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## Environment Variables Summary

### Backend (Railway)
```env
# Upstash Kafka
UPSTASH_KAFKA_BROKERS=xxx.upstash.io:9092
UPSTASH_KAFKA_USERNAME=xxx
UPSTASH_KAFKA_PASSWORD=xxx

# Upstash Redis
UPSTASH_REDIS_URL=redis://xxx.upstash.io:6379
UPSTASH_REDIS_TOKEN=xxx

# App Config
EVENTS_ENABLED=true
OPENAI_API_KEY=demo
```

### Frontend (Vercel)
```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

---

## Deliverables Achieved

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Cloud Deployed System | ✅ | Vercel + Railway + Upstash |
| Kafka Event Streaming | ✅ | Upstash Kafka (free) |
| Dapr Pub/Sub Pattern | ✅ | REST API compatible |
| Scalable AI Architecture | ✅ | Microservices + Events |
| CI/CD Pipeline | ✅ | GitHub Actions (free) |
| **Total Cost** | **$0** | All free tiers |

---

## One-Click Deploy Buttons

Add these to your README:

```markdown
[![Deploy Frontend to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/hackathon-todo&root-directory=hackathon-todo/frontend)

[![Deploy Backend to Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/hackathon-todo&root-directory=hackathon-todo/backend)
```

---

## Quick Commands

```bash
# Local development
cd hackathon-todo/backend && uvicorn main:app --reload
cd hackathon-todo/frontend && npm run dev

# Deploy (auto via GitHub push)
git push origin main
```

---

## Interview Ready Points

1. **Event-Driven Architecture** - Kafka for async communication
2. **Microservices** - Backend, Reminder Service, Frontend separated
3. **Cloud Native** - Serverless deployment on multiple platforms
4. **CI/CD** - Automated testing and deployment
5. **Scalability** - Each service scales independently
6. **Cost Optimization** - $0/month using free tiers
