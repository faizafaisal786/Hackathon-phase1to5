# 🚀 Quick Start - FREE Mode (No API Costs!)

This guide will help you run the Hackathon Todo app in **FREE demo mode** with **ZERO API costs**.

## ⚡ Super Fast Setup (1 Minute)

### Option 1: One-Command Start

```bash
python run.py
```

That's it! The script will:
- Check Python version
- Install missing dependencies
- Set up environment
- Initialize database
- Start the server

### Option 2: Manual Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn app.main:app --reload
```

## 🌐 Access the Application

Once started, open your browser:

- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs (Try the API here!)
- **Alternative Docs**: http://localhost:8000/redoc

## 💬 Try the FREE AI Chat (No API Key Needed!)

The app runs in **FREE demo mode** by default - no OpenAI API key required!

### Using cURL:

```bash
# Add a task
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Add a task to buy groceries\"}"

# List tasks
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Show me my tasks\"}"

# Complete a task
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Complete task ID: xyz\"}"
```

### Using the Interactive Docs:

1. Go to http://localhost:8000/docs
2. Find the **POST /chat/** endpoint
3. Click "Try it out"
4. Enter a message like: `"Add a task to prepare presentation"`
5. Click "Execute"

## 🎯 What You Can Say (Demo Mode)

The FREE demo mode understands these commands:

### Add Tasks
- "Add a task to buy groceries"
- "Create a new task: finish project"
- "Add task: call mom tomorrow"

### View Tasks
- "Show me my tasks"
- "List all tasks"
- "What tasks do I have?"
- "Show pending tasks"
- "Show completed tasks"

### Complete Tasks
- "Complete task ID: abc123"
- "Mark the first task as done"
- "Finish task xyz"

### Delete Tasks
- "Delete task ID: abc123"
- "Remove the grocery task"

## 🔄 REST API Endpoints

You can also use the traditional REST API:

### Authentication
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"user@example.com\",
    \"username\": \"testuser\",
    \"password\": \"password123\",
    \"full_name\": \"Test User\"
  }"

# Login
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"testuser\",
    \"password\": \"password123\"
  }"
```

### Tasks (with JWT token)
```bash
# Get token first, then:
TOKEN="your-jwt-token-here"

# List tasks
curl -X GET "http://localhost:8000/tasks" \
  -H "Authorization: Bearer $TOKEN"

# Create task
curl -X POST "http://localhost:8000/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Buy groceries\",
    \"description\": \"Milk, eggs, bread\",
    \"completed\": false
  }"
```

## 🎨 Frontend (Optional)

To run the Next.js frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend will be at: http://localhost:3000

## 🔐 Security Features

- JWT token authentication
- Password hashing with bcrypt
- Environment variable protection
- CORS configuration
- User-specific data isolation

## 📊 Database

- Uses SQLite by default (no setup needed!)
- Database file: `hackathon_todo.db`
- Automatically created on first run

## ⚙️ Configuration

The app uses `.env` file for configuration:

```env
# FREE demo mode (default)
OPENAI_API_KEY=demo

# Database
DATABASE_URL=sqlite:///./hackathon_todo.db

# JWT Secret (auto-generated)
SECRET_KEY=your-secret-key
```

## 🚀 Upgrade to AI Mode (Optional)

Want smarter AI responses? Get a FREE OpenAI API key:

1. Sign up at https://platform.openai.com/
2. Get $5 free credits (no card required initially)
3. Create an API key
4. Update `.env`:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
5. Restart the server

## 🛠️ Troubleshooting

### Port 8000 already in use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Dependencies not installing
```bash
# Upgrade pip first
python -m pip install --upgrade pip
# Then install dependencies
pip install -r requirements.txt
```

### Database errors
```bash
# Delete and recreate database
rm hackathon_todo.db
python run.py
```

## 📚 Features

✅ **FREE demo mode** - No API costs
✅ **AI-powered chat** - Natural language task management
✅ **REST API** - Full CRUD operations
✅ **Authentication** - Secure JWT tokens
✅ **Documentation** - Interactive Swagger UI
✅ **Database** - SQLite (auto-setup)
✅ **Professional** - Production-ready code

## 🎯 Next Steps

1. ✅ Start the server: `python run.py`
2. ✅ Open docs: http://localhost:8000/docs
3. ✅ Try the chat: POST to `/chat/`
4. ✅ Register a user via `/auth/register`
5. ✅ Create tasks via `/tasks`

## 🆘 Need Help?

- Check `AGENT_SETUP.md` for detailed setup
- Check `README.md` for full documentation
- Check `backend/README.md` for backend details
- Visit http://localhost:8000/docs for API documentation

---

**Ready to go! Just run:** `python run.py` 🚀
