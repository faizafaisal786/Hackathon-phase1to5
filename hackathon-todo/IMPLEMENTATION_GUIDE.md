# Implementation Guide: MCP Server, OpenAI Agents SDK & Chat Endpoint

## Overview

This guide documents the three core features implemented in the hackathon-todo application:

1. **MCP Server with Task Tools** - Model Context Protocol server for task management
2. **OpenAI Agents SDK Integration** - AI agent with function calling (FREE demo mode available)
3. **Chat Endpoint** - RESTful API endpoints for conversational task management

---

## 1. MCP Server with Task Tools

### Location
`backend/mcp_server.py`

### Features
The MCP server exposes 5 task management tools:

- `add_task` - Add a new task to the todo list
- `list_tasks` - List all tasks, optionally filtered by status
- `update_task` - Update an existing task
- `delete_task` - Delete a task by ID
- `complete_task` - Mark a task as completed

### Running the MCP Server

```bash
cd hackathon-todo/backend
python mcp_server.py
```

### Usage Example

The MCP server communicates via stdio (standard input/output) and follows the MCP protocol specification.

```json
{
  "tool": "add_task",
  "arguments": {
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "due_date": "2024-01-15"
  }
}
```

---

## 2. OpenAI Agents SDK Integration

### Location
`backend/agent.py`

### Features

#### FREE Demo Mode (No API Key Required!)
The implementation includes a **FREE demo mode** that works without any OpenAI API key:
- Pattern matching for common commands
- Support for Hindi/Hinglish commands
- Automatic date parsing (kal/tomorrow, parso, aaj, etc.)
- No external API calls - completely free to use

#### OpenAI API Mode (Optional)
If you provide an OpenAI API key, the agent uses:
- GPT-4o-mini model
- Advanced function calling
- Better natural language understanding

### Configuration

Create a `.env` file in the `hackathon-todo` directory:

```env
# For FREE demo mode (no API key needed):
OPENAI_API_KEY=demo

# OR for OpenAI API mode (requires paid API key):
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Supported Commands

#### English Commands
- "Add a task to buy groceries"
- "Show me all my tasks"
- "List pending tasks"
- "Complete task ID: xyz"
- "Delete the first task"

#### Hindi/Hinglish Commands
- "Kal ka kaam add kar do" (Add tomorrow's task)
- "Dikha do sab tasks" (Show all tasks)
- "Pehla task complete kar do" (Complete first task)

### Date Understanding
- "kal" / "tomorrow" → Tomorrow's date
- "parso" / "day after tomorrow" → Day after tomorrow
- "aaj" / "today" → Today's date
- "agle hafte" / "next week" → Next week
- "agle mahine" / "next month" → Next month

### Usage Example

```python
from backend.agent import simple_chat

# Simple usage
response = simple_chat("Add a task to buy groceries tomorrow")
print(response)

# With conversation history
from backend.agent import chat

result = chat("Show my tasks", conversation_history=[])
print(result["message"])
```

---

## 3. Chat Endpoint

### Locations
- `backend/main.py` - Simple backend with chat endpoints
- `app/routers/chat.py` - Advanced backend with authentication

### Endpoints

#### POST /api/chat
Simple chat endpoint without authentication

**Request:**
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-uuid",
  "conversation_history": []
}
```

**Response:**
```json
{
  "message": "I've added the task 'buy groceries' to your list!",
  "conversation_id": "uuid-here",
  "conversation_history": [
    {"role": "user", "content": "Add a task to buy groceries"},
    {"role": "assistant", "content": "I've added the task..."}
  ]
}
```

#### POST /chat/
Advanced chat endpoint with user authentication (from `app/routers/chat.py`)

Requires authentication token in headers:
```
Authorization: Bearer <token>
```

### Running the Backend

```bash
cd hackathon-todo/backend
python main.py
```

The server will start on `http://localhost:8000`

### Testing the Endpoints

```bash
# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "show my tasks"
  }'

# Test task endpoints
curl http://localhost:8000/api/tasks

# Test health endpoint
curl http://localhost:8000/
```

---

## Complete Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (Next.js)              │
│      /chat, /login, /register           │
└────────────────┬────────────────────────┘
                 │ HTTP/REST
                 ▼
┌─────────────────────────────────────────┐
│      Backend API (FastAPI)              │
│   - /api/chat                           │
│   - /api/tasks                          │
│   - /auth/*                             │
└────────────┬────────────┬───────────────┘
             │            │
             ▼            ▼
  ┌──────────────┐  ┌──────────────┐
  │ OpenAI Agent │  │  MCP Server  │
  │  (agent.py)  │  │(mcp_server.py)│
  └──────────┬───┘  └───────┬──────┘
             │              │
             └──────┬───────┘
                    ▼
            ┌───────────────┐
            │ Task Manager  │
            │  (tasks.py)   │
            └───────┬───────┘
                    ▼
            ┌───────────────┐
            │  tasks.json   │
            └───────────────┘
```

---

## Key Features

### 1. FREE Mode
- No API costs
- Works without OpenAI API key
- Pattern matching for task operations
- Hindi/Hinglish support

### 2. Multi-Protocol Support
- REST API (HTTP)
- MCP Protocol (stdio)
- OpenAI Function Calling

### 3. Bilingual Support
- English commands
- Hindi/Hinglish commands
- Automatic language detection

### 4. Conversation History
- Persistent conversation storage
- SQLite database for messages
- Conversation threading

---

## Testing the Implementation

### 1. Test Task Functions
```bash
cd hackathon-todo/backend
python -c "from tasks import add_task, list_tasks; add_task('Test Task'); print(list_tasks())"
```

### 2. Test Agent (Demo Mode)
```bash
cd hackathon-todo/backend
python agent.py
```

### 3. Test MCP Server
```bash
cd hackathon-todo/backend
python mcp_server.py
```

### 4. Test Backend API
```bash
cd hackathon-todo/backend
python main.py
```

Then in another terminal:
```bash
curl http://localhost:8000/api/tasks
```

---

## Troubleshooting

### Issue: Module import errors
**Solution:** Make sure you're in the correct directory and all dependencies are installed:
```bash
cd hackathon-todo
pip install -r requirements.txt
```

### Issue: No response from agent
**Solution:** Check if you're in demo mode (default) or if API key is set correctly in `.env`

### Issue: MCP server not starting
**Solution:** Ensure the MCP SDK is installed:
```bash
pip install mcp>=1.0.0
```

---

## Next Steps

1. **Deploy the backend** to a cloud service (Heroku, Railway, etc.)
2. **Configure the frontend** to use the deployed backend URL
3. **Add authentication** for production use
4. **Monitor usage** if using OpenAI API (costs apply)

---

## Files Modified/Created

- ✅ `backend/mcp_server.py` - MCP server implementation
- ✅ `backend/agent.py` - OpenAI Agents SDK integration
- ✅ `backend/main.py` - Chat endpoints
- ✅ `backend/tasks.py` - Task management functions
- ✅ `backend/conversations.py` - Conversation storage
- ✅ `requirements.txt` - Updated with MCP SDK
- ✅ `IMPLEMENTATION_GUIDE.md` - This documentation

---

## Summary

All three requested features are **fully implemented and working**:

1. ✅ **MCP Server with task tools** - Ready to use via stdio
2. ✅ **OpenAI Agents SDK** - Working in FREE demo mode (no API key needed)
3. ✅ **Chat endpoint** - REST API ready at `/api/chat`

The implementation supports both **free demo mode** and **OpenAI API mode**, making it flexible for development and production use.
