# Deployment Guide: Vercel (Frontend) + Railway (Backend)

Free tier deployment guide for PR preview deployments.

## Step 1: Deploy Backend on Railway

### 1.1 Create Railway Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub

### 1.2 Deploy Backend
**Option A: Using Railway CLI**
```bash
npm install -g @railway/cli
railway login
cd hackathon-todo/backend
railway init
railway up
```

**Option B: Using GitHub Integration (Recommended)**
1. Go to Railway Dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Set Root Directory: `hackathon-todo/backend`
6. Railway will auto-detect Python and deploy

### 1.3 Set Environment Variables on Railway
In Railway Dashboard > Variables:
```
OPENAI_API_KEY=demo
```
(PORT is auto-set by Railway)

### 1.4 Get Backend URL
After deployment, copy the URL:
```
https://your-app-name.up.railway.app
```

---

## Step 2: Deploy Frontend on Vercel

### 2.1 Create Vercel Account
- Go to [vercel.com](https://vercel.com)
- Sign up with GitHub

### 2.2 Deploy Frontend
**Using Vercel Dashboard:**
1. Go to Vercel Dashboard
2. Click "Add New" > "Project"
3. Import your GitHub repository
4. Set Root Directory: `hackathon-todo/frontend`
5. Framework Preset: Next.js (auto-detected)

### 2.3 Set Environment Variables on Vercel
In Vercel Dashboard > Settings > Environment Variables:
```
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
```

### 2.4 Redeploy
After setting environment variables, redeploy to apply changes.

---

## PR Preview Deployments

### Vercel (Automatic)
- Every PR automatically gets a preview deployment
- URL format: `https://your-project-git-branch-name.vercel.app`

### Railway
Railway free tier supports only one deployment.
All preview deployments will use the same backend URL.

---

## Environment Variables Summary

### Backend (Railway)
| Variable | Value |
|----------|-------|
| `OPENAI_API_KEY` | Your API key or `demo` |

### Frontend (Vercel)
| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | Railway backend URL |

---

## Quick Deploy Commands

### Using CLIs
```bash
# Backend (Railway)
cd hackathon-todo/backend
railway up

# Frontend (Vercel)
cd hackathon-todo/frontend
vercel
```

---

## Troubleshooting

### CORS Errors
Backend has CORS configured to allow all origins (`*`).

### 500 Errors
Check Railway logs:
```bash
railway logs
```

### Build Failures
Check Vercel deployment logs in dashboard.

---

## URLs After Deployment
- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-project.up.railway.app`
- **API Health**: `https://your-project.up.railway.app/health`
