# Phase 5 - Cloud Deployment (100% FREE)

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 5 ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User Browser                                               │
│        │                                                     │
│        ▼                                                     │
│   ┌─────────────┐      ┌─────────────┐                      │
│   │   Vercel    │      │   Vercel    │                      │
│   │  Frontend   │ ───► │  Backend    │                      │
│   │  (Next.js)  │      │  (FastAPI)  │                      │
│   └─────────────┘      └─────────────┘                      │
│                              │                               │
│                              ▼                               │
│                        ┌─────────────┐                      │
│                        │   SQLite    │                      │
│                        │  Database   │                      │
│                        └─────────────┘                      │
│                                                              │
│   Cost: $0/month (100% FREE)                                │
└─────────────────────────────────────────────────────────────┘
```

## Live URLs

| Service | URL |
|---------|-----|
| Frontend | https://hackathon-todo.vercel.app |
| Backend API | https://backend-flax-seven-28.vercel.app |
| API Docs | https://backend-flax-seven-28.vercel.app/docs |

## How It Works

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to cloud"
git push origin main
```

### Step 2: Automatic CI/CD
GitHub Actions automatically:
1. Runs tests
2. Builds frontend
3. Deploys to Vercel

### Step 3: Access Your App
Open: https://hackathon-todo.vercel.app

## Features Available (FREE)

| Feature | Status |
|---------|--------|
| Task CRUD | Working |
| AI Chat (Demo Mode) | Working |
| Multi-language (EN/HI/UR) | Working |
| User Authentication | Working |
| Responsive UI | Working |

## GitHub Secrets Required

For automated deployment, add these secrets in GitHub:

```
Settings → Secrets and variables → Actions → New repository secret
```

| Secret | How to Get |
|--------|------------|
| VERCEL_TOKEN | https://vercel.com/account/tokens |
| VERCEL_ORG_ID | Vercel Dashboard → Settings → General |
| VERCEL_PROJECT_ID | Vercel Project → Settings → General |

## Manual Deploy (Without CI/CD)

### Option 1: Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy Frontend
cd hackathon-todo/frontend
vercel --prod

# Deploy Backend
cd hackathon-todo/backend
vercel --prod
```

### Option 2: Vercel Dashboard
1. Go to https://vercel.com
2. Import GitHub repository
3. Configure root directory
4. Deploy!

## Technology Stack

| Component | Technology | Cost |
|-----------|------------|------|
| Frontend | Next.js 14 | FREE |
| Backend | FastAPI | FREE |
| Database | SQLite | FREE |
| AI Chat | Demo Mode | FREE |
| Hosting | Vercel | FREE |
| CI/CD | GitHub Actions | FREE |

## Troubleshooting

### CORS Error
Backend already configured to allow all origins with:
```python
allow_origins=["*"]
```

### Build Failed
Check GitHub Actions logs for details.

### API Not Responding
Check backend health: https://backend-flax-seven-28.vercel.app/health

## Summary

```
Phase 5 = Git Push → Auto Deploy → Live App

No localhost needed!
No manual server management!
100% FREE hosting!
```
