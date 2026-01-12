# Quick Deploy to Vercel - Complete Guide

## 🚀 Complete Deployment in 10 Minutes (FREE!)

This guide will help you deploy both frontend and backend to Vercel for FREE using demo mode (no API key required).

## Step 1: Deploy Backend (FREE Demo Mode)

### 1.1 Go to Vercel Dashboard
1. Visit [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "Add New Project" → "Import Project"
3. Select your GitHub repository

### 1.2 Configure Backend
- **Root Directory**: `hackathon-todo/backend`
- **Framework**: Other
- **Build Command**: Leave empty
- **Output Directory**: Leave empty

### 1.3 Add Environment Variable
Click "Environment Variables" and add:
- **Key**: `OPENAI_API_KEY`
- **Value**: `demo` (for FREE mode, no API key needed!)

### 1.4 Deploy
1. Click "Deploy"
2. Wait for deployment to complete (2-3 minutes)
3. **COPY YOUR BACKEND URL** (e.g., `https://your-backend.vercel.app`)

---

## Step 2: Deploy Frontend

### 2.1 Go to Vercel Dashboard
1. Click "Add New Project" again
2. Select the same repository (or click "Import" again)

### 2.2 Configure Frontend
- **Root Directory**: `hackathon-todo/frontend`
- **Framework**: Next.js (auto-detected)
- **Build Command**: `npm run build` (auto-filled)
- **Output Directory**: `.next` (auto-filled)

### 2.3 Add Environment Variable
Click "Environment Variables" and add:
- **Key**: `NEXT_PUBLIC_API_URL`
- **Value**: YOUR BACKEND URL from Step 1 (e.g., `https://your-backend.vercel.app`)

### 2.4 Deploy
1. Click "Deploy"
2. Wait for deployment to complete (3-5 minutes)
3. **COPY YOUR FRONTEND URL** (e.g., `https://your-frontend.vercel.app`)

---

## Step 3: Test Your App

Open your frontend URL and test:
1. Click "Register" to create an account
2. Login with your credentials
3. Try adding tasks
4. Try the chat feature: "Add a task to buy groceries"
5. Test Hindi/Hinglish: "Kal ka kaam add kar do"

---

## Quick Troubleshooting

### Frontend shows 404
- Check Root Directory is set to `hackathon-todo/frontend`
- Verify build completed successfully in deployment logs

### Frontend can't connect to backend
- Check `NEXT_PUBLIC_API_URL` is set correctly
- Make sure you used the FULL backend URL including `https://`
- Redeploy frontend after adding environment variable

### Backend 500 error
- Check Function Logs in Vercel dashboard
- Verify `OPENAI_API_KEY` is set to `demo`
- Try redeploying

---

## What You Get (FREE!)

✅ **Backend API** - FastAPI with all task management endpoints
✅ **Frontend** - Next.js modern UI with authentication
✅ **AI Chat Agent** - Works in FREE demo mode (no API key!)
✅ **Hindi/Hinglish Support** - Understands local language commands
✅ **Auto HTTPS** - Secure by default
✅ **Auto Scaling** - Handles traffic automatically

---

## Demo Mode Features (FREE)

Your app will support these commands in demo mode:

**English:**
- "Add a task to buy groceries"
- "Show me my tasks"
- "Complete task ID: xyz"
- "Delete the first task"

**Hindi/Hinglish:**
- "Kal ka kaam add kar do" (Add tomorrow's task)
- "Tasks dikha do" (Show tasks)
- "Kaam complete kar do" (Complete task)

---

## Want Full AI Features?

To use OpenAI's GPT-4o-mini for smarter AI responses:

1. Get an OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Go to Backend project → Settings → Environment Variables
3. Change `OPENAI_API_KEY` from `demo` to your actual key
4. Redeploy backend

**Note:** This will incur OpenAI API costs based on usage.

---

## Important Notes

### Data Persistence
⚠️ Current implementation uses local file storage which **doesn't persist** in Vercel's serverless environment.

For production:
- Use a cloud database (Vercel Postgres, Supabase, etc.)
- Use cloud storage (Vercel Blob, S3, etc.)

### CORS
Backend allows all origins (`*`) for development. For production, update `main.py`:
```python
allow_origins=["https://your-frontend.vercel.app"]
```

---

## URLs to Save

After deployment, save these:
- **Backend URL**: `https://your-backend.vercel.app`
- **Frontend URL**: `https://your-frontend.vercel.app`

---

## Need Help?

1. Check deployment logs in Vercel dashboard
2. Check Function Logs for runtime errors
3. See detailed guides:
   - Frontend: `hackathon-todo/frontend/VERCEL_DEPLOYMENT.md`
   - Backend: `hackathon-todo/backend/VERCEL_DEPLOYMENT.md`

---

## Cost Breakdown

| Service | Cost |
|---------|------|
| Vercel Hosting (Frontend) | FREE (Hobby plan) |
| Vercel Hosting (Backend) | FREE (Hobby plan) |
| OpenAI API (Demo Mode) | FREE (no API calls) |
| OpenAI API (Full Mode) | Pay per use (~$0.15/1M tokens) |

**Total for Demo Mode: $0/month** 🎉

---

Happy deploying! 🚀
