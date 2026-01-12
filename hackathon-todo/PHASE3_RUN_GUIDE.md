# Phase 3 Run Guide - AI Chat Integration

## Overview
Phase 3 integrates AI chat functionality where users can chat with an AI agent that automatically manages tasks using natural language commands in both English and Hindi/Hinglish.

## Architecture Flow
```
User → Chat UI (Frontend)
  ↓
Chat → AI Agent (Backend)
  ↓
AI → Tool (add_task, list_tasks, etc.)
  ↓
Tool → Backend API (/api/tasks)
```

## Step 1: Run Backend + AI

### Prerequisites
- Python 3.8+
- Install dependencies:
```bash
cd hackathon-todo/backend
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file in the `backend` directory (optional):
```env
OPENAI_API_KEY=your_api_key_here
# OR leave empty/use "demo" for demo mode (no API key required)
OPENAI_API_KEY=demo
```

### Start Backend
```bash
cd hackathon-todo/backend
uvicorn main:app --reload
```

Backend will run on: `http://localhost:8000`

**Available Endpoints:**
- `/api/tasks` - Task CRUD operations
- `/api/chat` - AI chat endpoint
- `/chat/` - Alternative chat endpoint (for frontend compatibility)

## Step 2: Run Frontend

### Prerequisites
- Node.js 18+
- Install dependencies:
```bash
cd hackathon-todo/frontend
npm install
```

### Start Frontend
```bash
cd hackathon-todo/frontend
npm run dev
```

Frontend will run on: `http://localhost:3000`

## Step 3: Using the Chat Feature

### Access Chat UI
1. Navigate to `http://localhost:3000`
2. Login/Register (if authentication is enabled)
3. Go to the Chat page: `http://localhost:3000/chat`

### Example Commands

#### English Commands:
- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark task 1 as complete"
- "Delete the grocery task"
- "Add a task for tomorrow"

#### Hindi/Hinglish Commands:
- "Kal ka kaam add kar do" (Add tomorrow's work)
- "Aaj ka kaam dikhao" (Show today's work)
- "Grocery ka kaam add karo" (Add grocery task)
- "Saare kaam dikhao" (Show all tasks)

### How It Works

1. **User sends message**: "Kal ka kaam add kar do"
2. **AI Agent processes**: Extracts "kaam" as title and "kal" (tomorrow) as due date
3. **AI calls tool**: `add_task(title="kaam", due_date="2024-01-06")`
4. **Tool executes**: Calls backend `/api/tasks` endpoint
5. **Task created**: Saved to `tasks.json`
6. **AI responds**: "I've added the task 'kaam' with due date tomorrow!"

## Features

### AI Agent Capabilities
- ✅ Natural language understanding (English + Hindi/Hinglish)
- ✅ Automatic task creation from chat
- ✅ Date parsing ("kal", "tomorrow", "parso", etc.)
- ✅ Task listing and management
- ✅ Task completion and deletion

### Demo Mode
If no OpenAI API key is provided, the system runs in **FREE demo mode** using pattern matching. This works for basic commands but may not understand complex natural language.

### Full AI Mode
With an OpenAI API key, the system uses GPT-4o-mini for advanced natural language understanding and can handle complex queries.

## Troubleshooting

### Backend Issues
- **Port already in use**: Change port in `main.py` or kill existing process
- **Import errors**: Make sure you're in the `backend` directory when running
- **Tasks file not found**: The file will be created automatically on first task

### Frontend Issues
- **API connection failed**: Check backend is running on `http://localhost:8000`
- **CORS errors**: Backend CORS is configured to allow all origins (for development)
- **Chat not responding**: Check backend logs for errors

### AI Not Working
- **Demo mode**: Works with basic pattern matching (limited)
- **Full AI mode**: Requires valid OpenAI API key in `.env` file
- **Rate limits**: Check OpenAI API usage if you hit rate limits

## Testing

### Test Chat Flow
1. Open chat UI
2. Type: "Kal ka kaam add kar do"
3. Should see: Task created confirmation
4. Type: "Saare kaam dikhao"
5. Should see: List of all tasks including the one just created

### Test Backend Directly
```bash
# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk", "conversation_id": "test123"}'

# Test tasks endpoint
curl http://localhost:8000/api/tasks
```

## Next Steps

- Add more sophisticated date parsing
- Implement conversation history persistence
- Add task priority and categories
- Enhance AI understanding for complex queries
- Add voice input support

