# ⚡ QUICK FIX - Login Failed Error

## The Problem
Your frontend is deployed but can't connect to the backend.
**Error:** "Login failed. Please check your credentials."

## The Fix (5 Minutes)

### 🎯 Step 1: Deploy Backend

1. Go to: **https://vercel.com/dashboard**
2. Click: **"Add New Project"**
3. Select: Your GitHub repository
4. Set: **Root Directory** = `hackathon-todo/backend`
5. Add Environment Variable:
   - Name: `OPENAI_API_KEY`
   - Value: `demo`
6. Click: **"Deploy"**
7. **COPY the deployment URL** (looks like: `https://something.vercel.app`)

---

### 🎯 Step 2: Connect Frontend to Backend

1. Go to: **https://vercel.com/dashboard**
2. Click: Your **frontend** project (frontend-neon-theta-22)
3. Click: **"Settings"** → **"Environment Variables"**
4. Click: **"Add New"**
5. Add:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: [Your backend URL from Step 1]
   - Example: `https://hackathon-backend-abc123.vercel.app`
6. Click: **"Save"**
7. Go to: **"Deployments"** tab
8. Click: **"..."** on latest deployment → **"Redeploy"**

---

### 🎯 Step 3: Test

1. Wait 2-3 minutes for redeployment
2. Visit: **https://frontend-neon-theta-22.vercel.app/test**
3. Check: Should show "✅ Connected! Backend is working"
4. Go to: **https://frontend-neon-theta-22.vercel.app/login**
5. Login with ANY username/password (e.g., test/test)
6. ✅ Should work!

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---------|-----|
| Root directory = `hackathon-todo` | Must be `hackathon-todo/backend` |
| Env var name = `API_URL` | Must be `NEXT_PUBLIC_API_URL` |
| Forgot to redeploy frontend | Must redeploy after adding env var |
| Backend URL has trailing `/` | Remove it: `...vercel.app` not `...vercel.app/` |

---

## 🚨 Still Not Working?

1. Visit: `/test` page to check connection status
2. Check browser console (F12) for errors
3. See full guide: `TROUBLESHOOTING.md`

---

## ✅ Verification Checklist

- [ ] Backend deployed successfully
- [ ] Backend URL copied
- [ ] Frontend env var `NEXT_PUBLIC_API_URL` added
- [ ] Frontend redeployed
- [ ] `/test` page shows backend connected
- [ ] Login works with any credentials

---

**That's it! Your app should be working now.** 🎉
