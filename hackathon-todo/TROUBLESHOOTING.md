# 🔧 Troubleshooting Guide - Login Failed Error

## Problem: "Login failed. Please check your credentials"

This error occurs when the **frontend cannot connect to the backend**. The backend is either:
1. Not deployed yet
2. Not configured in the frontend environment variables

---

## ✅ Solution (Step by Step)

### Step 1: Check Backend Deployment Status

**Option A - Check if Backend is Deployed:**
```
Go to: https://vercel.com/dashboard
Look for: A project with "backend" in the name
```

**Option B - Test Backend URL (if you have it):**
```
Open in browser: https://your-backend-url.vercel.app/
Expected: Should show {"message": "Todo App Backend with AI", ...}
```

---

### Step 2: If Backend is NOT Deployed - Deploy it Now

1. **Go to Vercel Dashboard**
   - URL: https://vercel.com/dashboard
   - Click "Add New Project"

2. **Import Repository**
   - Select your GitHub repository
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `hackathon-todo/backend` ⚠️ IMPORTANT!
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

4. **Add Environment Variable**
   - Click "Environment Variables"
   - Add New:
     - **Name**: `OPENAI_API_KEY`
     - **Value**: `demo`
   - Click "Add"

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - **COPY YOUR BACKEND URL** (e.g., `https://hackathon-backend-xyz.vercel.app`)

---

### Step 3: Configure Frontend with Backend URL

1. **Go to Frontend Project on Vercel**
   - Go to: https://vercel.com/dashboard
   - Click on your frontend project (the one showing https://frontend-neon-theta-22.vercel.app)

2. **Open Settings**
   - Click "Settings" tab
   - Click "Environment Variables" in left sidebar

3. **Add Backend URL**
   - Click "Add New"
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your backend URL from Step 2 (e.g., `https://hackathon-backend-xyz.vercel.app`)
   - **Important**: Do NOT add trailing slash!
   - Click "Save"

4. **Redeploy Frontend**
   - Go to "Deployments" tab
   - Click the 3 dots (...) on the latest deployment
   - Click "Redeploy"
   - Wait 2-3 minutes

---

### Step 4: Test the Fix

1. **Visit Test Page**
   ```
   https://frontend-neon-theta-22.vercel.app/test
   ```
   This page will show:
   - If NEXT_PUBLIC_API_URL is set ✅
   - If backend is reachable ✅

2. **If Test Page Shows Success:**
   - Go to: https://frontend-neon-theta-22.vercel.app/login
   - Try logging in with ANY username and password
   - It should work! (Stub accepts all credentials)

---

## 🐛 Common Mistakes

### Mistake 1: Wrong Root Directory
**Problem:** Set root to `hackathon-todo` instead of `hackathon-todo/backend`
**Fix:** Settings → General → Root Directory → Change to `hackathon-todo/backend`

### Mistake 2: Missing Environment Variable
**Problem:** Forgot to add `NEXT_PUBLIC_API_URL` to frontend
**Fix:** Follow Step 3 above

### Mistake 3: Wrong Environment Variable Name
**Problem:** Used `API_URL` instead of `NEXT_PUBLIC_API_URL`
**Fix:** Must start with `NEXT_PUBLIC_` for Next.js client-side access

### Mistake 4: Trailing Slash in URL
**Problem:** Backend URL like `https://backend.vercel.app/`
**Fix:** Remove trailing slash: `https://backend.vercel.app`

### Mistake 5: Using HTTP instead of HTTPS
**Problem:** `http://backend.vercel.app`
**Fix:** Use `https://backend.vercel.app`

---

## 🔍 Quick Diagnostic

### Test Backend is Working:
```bash
# Replace with your backend URL
curl https://your-backend.vercel.app/

# Expected output:
# {"message":"Todo App Backend with AI","endpoints":[...]}
```

### Test Frontend Environment Variable:
```
Visit: https://frontend-neon-theta-22.vercel.app/test
```

### Check Browser Console:
1. Open frontend in browser
2. Press F12 (Developer Tools)
3. Go to "Console" tab
4. Look for errors with:
   - "CORS"
   - "Network Error"
   - "localhost:8000"

**If you see "localhost:8000":**
→ Environment variable is NOT set or NOT deployed yet!

---

## 📋 Checklist

Before login can work, verify:
- [ ] Backend deployed to Vercel
- [ ] Backend URL copied (e.g., `https://backend-xyz.vercel.app`)
- [ ] Backend URL tested in browser (shows API info)
- [ ] Frontend env var `NEXT_PUBLIC_API_URL` added
- [ ] Frontend redeployed after adding env var
- [ ] Test page shows backend connected: `/test`
- [ ] No "localhost:8000" in browser console

---

## 🚨 Still Not Working?

### Check Vercel Function Logs:

1. **Backend Logs:**
   - Go to Backend project → Deployments
   - Click on latest deployment
   - Click "View Function Logs"
   - Look for errors

2. **Frontend Logs:**
   - Go to Frontend project → Deployments
   - Click on latest deployment
   - Click "View Function Logs"
   - Look for build/runtime errors

### Check CORS:

The backend should have this in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Clear Browser Cache:

1. Open Developer Tools (F12)
2. Right-click refresh button
3. Select "Empty Cache and Hard Reload"

---

## 💡 Expected Behavior

Once fixed:
1. Login page accepts ANY username/password (it's a stub)
2. After login, redirects to `/tasks`
3. Can add/view tasks
4. Can chat with AI agent

---

## 📞 Quick Commands

```bash
# Test backend
curl https://your-backend-url.vercel.app/

# Test login endpoint
curl -X POST https://your-backend-url.vercel.app/auth/token \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "username=test&password=test"

# Should return:
# {"access_token":"dummy_token_...","token_type":"bearer"}
```

---

## 🎯 Summary

**Root Cause:** Frontend trying to connect to `localhost:8000` instead of deployed backend.

**Solution:** Deploy backend → Copy URL → Add to frontend env var → Redeploy frontend.

**Test:** Visit `/test` page to verify connection.

---

Need more help? Check:
- `DEPLOY_TO_VERCEL.md` - Complete deployment guide
- `backend/VERCEL_DEPLOYMENT.md` - Backend specific guide
- `frontend/VERCEL_DEPLOYMENT.md` - Frontend specific guide
