# ☁️ Cloud Deployment Setup (100% FREE)

> **Ab tumhara laptop sirf viewer hai!**
> `git push origin main` = App Live 🚀

---

## 🎯 Final Result

```
git push origin main
     ↓
GitHub Actions (auto)
     ↓
🌐 https://your-app.vercel.app (Live!)
```

**No localhost. Real production. FREE.**

---

## 📋 One-Time Setup (15 minutes)

### Step 1: Upstash Account (FREE) - 2 min

1. Go to **[upstash.com](https://upstash.com)**
2. Sign up with GitHub
3. **Create Kafka:**
   - Click "Create Cluster"
   - Name: `hackathon-todo`
   - Region: Any
   - Copy: `UPSTASH_KAFKA_URL`, `USERNAME`, `PASSWORD`

4. **Create Redis:**
   - Click "Create Database"
   - Name: `hackathon-todo-redis`
   - Copy: `UPSTASH_REDIS_URL`

---

### Step 2: Railway Account (FREE) - 5 min

1. Go to **[railway.app](https://railway.app)**
2. Sign up with GitHub
3. **Create Project:**
   - New Project → Empty Project
   - Add Service → GitHub Repo → Select your repo
   - Root Directory: `hackathon-todo/backend`
   - Click Deploy

4. **Add Environment Variables:**
   ```
   UPSTASH_KAFKA_URL=https://xxx.upstash.io
   UPSTASH_KAFKA_USERNAME=xxx
   UPSTASH_KAFKA_PASSWORD=xxx
   EVENTS_ENABLED=true
   OPENAI_API_KEY=demo
   ```

5. **Get Railway Token:**
   - Account Settings → Tokens → Create Token
   - Copy the token

6. **Copy Backend URL** (e.g., `https://xxx.railway.app`)

---

### Step 3: Vercel Account (FREE) - 3 min

1. Go to **[vercel.com](https://vercel.com)**
2. Sign up with GitHub
3. **Import Project:**
   - Add New → Project
   - Import your GitHub repo
   - Root Directory: `hackathon-todo/frontend`
   - Add Environment Variable:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.railway.app
     ```
   - Deploy

4. **Get Vercel Credentials:**
   - Settings → Tokens → Create Token → Copy `VERCEL_TOKEN`
   - Project Settings → General → Copy `Project ID`
   - Account Settings → Copy `Team ID` (or personal account ID)

---

### Step 4: GitHub Secrets - 2 min

Go to your **GitHub Repo → Settings → Secrets → Actions**

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `VERCEL_TOKEN` | Your Vercel token |
| `VERCEL_ORG_ID` | Your Vercel Team/Account ID |
| `VERCEL_PROJECT_ID` | Your Vercel Project ID |
| `RAILWAY_TOKEN` | Your Railway token |

---

## 🚀 Deploy (Every Time)

```bash
# Make changes to code
git add .
git commit -m "Update feature"
git push origin main
```

**That's it! GitHub Actions automatically:**
1. ✅ Tests code
2. ✅ Builds Docker images
3. ✅ Deploys to Vercel (frontend)
4. ✅ Deploys to Railway (backend)
5. ✅ App is LIVE!

---

## 🌐 Your URLs (After Setup)

| Service | URL |
|---------|-----|
| **Frontend** | `https://your-project.vercel.app` |
| **Backend API** | `https://your-project.railway.app` |
| **Health Check** | `https://your-project.railway.app/health` |

---

## 📊 Architecture (Cloud)

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR LAPTOP                           │
│                  (Just Browser!)                         │
│                                                          │
│    Opens: https://hackathon-todo.vercel.app             │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 VERCEL CLOUD (FREE)                      │
│                                                          │
│    ┌─────────────────────────────────┐                  │
│    │     Next.js Frontend            │                  │
│    │     (Auto-scaled globally)      │                  │
│    └─────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                RAILWAY CLOUD (FREE)                      │
│                                                          │
│    ┌──────────────────┐  ┌──────────────────┐          │
│    │  Backend API     │  │ Reminder Service │          │
│    │  (FastAPI)       │  │ (Cron Job)       │          │
│    └──────────────────┘  └──────────────────┘          │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                UPSTASH CLOUD (FREE)                      │
│                                                          │
│    ┌──────────────────┐  ┌──────────────────┐          │
│    │  Kafka           │  │  Redis           │          │
│    │  (Events)        │  │  (State)         │          │
│    └──────────────────┘  └──────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Checklist

- [ ] Upstash account created
- [ ] Kafka cluster created
- [ ] Redis database created
- [ ] Railway account created
- [ ] Backend deployed on Railway
- [ ] Vercel account created
- [ ] Frontend deployed on Vercel
- [ ] GitHub secrets added
- [ ] `git push origin main` tested
- [ ] App live on cloud URL! 🎉

---

## 💰 Cost

| Service | Monthly Cost |
|---------|-------------|
| Vercel | $0 |
| Railway | $0 (free credit) |
| Upstash Kafka | $0 |
| Upstash Redis | $0 |
| GitHub Actions | $0 |
| **TOTAL** | **$0** |

---

## 🎉 You Did It!

```
Before: localhost:3000 (only your laptop)
After:  https://your-app.vercel.app (whole world!)
```

**Ab tumhara laptop sirf viewer hai - App cloud mein hai!** 🚀
