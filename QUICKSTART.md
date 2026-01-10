# ⚡ Quick Start - Get Running in 5 Minutes

## 🎯 Choose Your Path

Select which phase you want to run:

---

## 🚀 Option 1: Phase 1 (CLI - Fastest!)

### Run Locally
```bash
cd todo-phase1
python src/main.py
```

That's it! The menu will appear. ✅

### Deploy to Web (2 minutes)
```bash
cd todo-phase1
vercel --prod
```

Follow prompts, get live URL! 🌐

---

## 🌐 Option 2: Phase 2 (Full Stack - Recommended!)

### Backend (30 seconds)
```bash
cd hackathon-todo
python run.py
```

Visit: http://localhost:8000/docs ✅

### Frontend (1 minute)
Open new terminal:
```bash
cd hackathon-todo/frontend
npm install
npm run dev
```

Visit: http://localhost:3000 ✅

### Quick Test (30 seconds)
1. Go to http://localhost:3000
2. Click "Register"
3. Create account
4. Add a task!

Done! 🎉

---

## 🤖 Option 3: Phase 3 (AI Chat - Most Fun!)

### Start Backend with AI
```bash
cd hackathon-todo
python run.py
```

### Try AI Chat
1. Visit: http://localhost:8000/docs
2. Find `/chat` endpoint
3. Click "Try it out"
4. Send: "Add a task to buy groceries"
5. See AI response! 🤖

---

## 🐳 Option 4: Phase 4 (Docker - Most Professional!)

### One Command
```bash
cd hackathon-todo
docker-compose up
```

Wait 30 seconds, then:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

Done! 🎉

---

## 🆘 Troubleshooting

### Port Already in Use?
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Backend Won't Start?
```bash
cd hackathon-todo
python test_app.py
```

If tests pass, backend is fine. Check your Python version (need 3.10+).

### Frontend Won't Start?
```bash
cd hackathon-todo/frontend
rm -rf node_modules
npm install
npm run dev
```

### Docker Issues?
Make sure Docker Desktop is running!

---

## 📋 What's Next?

After getting it running:

1. ✅ **Test It**: Play with the app
2. 📚 **Read**: Check README.md for full docs
3. 🚀 **Deploy**: Follow DEPLOYMENT_GUIDE.md
4. 🎬 **Record**: Make demo videos
5. 🏆 **Submit**: Use WINNING_CHECKLIST.md

---

## 🎯 Most Common Workflows

### Just Want to See It Work?
```bash
cd hackathon-todo
python run.py
```
Then visit http://localhost:8000/docs

### Want Full Experience?
Run both backend AND frontend (see Option 2 above)

### Want to Deploy?
```bash
# Use the automated script
./deploy.bat    # Windows
./deploy.sh     # Mac/Linux
```

---

## 📞 Need Help?

Check these files in order:
1. This file (QUICKSTART.md)
2. HACKATHON_RUN_GUIDE.md
3. README.md
4. DEPLOYMENT_GUIDE.md

---

## ✅ Success Checklist

- [ ] Phase 1 CLI running
- [ ] Phase 2 Backend running (http://localhost:8000)
- [ ] Phase 2 Frontend running (http://localhost:3000)
- [ ] Registered a test user
- [ ] Created a test task
- [ ] Tested AI chat (/chat endpoint)
- [ ] Read README.md
- [ ] Ready to deploy!

---

**Happy Coding! 🚀**

*Get running fast, deploy faster, win fastest!*
