# AI Agent Setup and Usage Guide

This guide explains how to set up and use the AI agent features of the Hackathon Todo application.

## Overview

The application now includes three AI-powered components:

1. **MCP Server** - Exposes task management tools via Model Context Protocol
2. **OpenAI Agent** - Natural language interface using OpenAI's function calling
3. **Chat API Endpoint** - RESTful API for the AI agent

## Prerequisites

- Python 3.10+
- OpenAI API key (for the agent and chat endpoint)
- All dependencies from `requirements.txt` and `backend/requirements.txt`

## Installation

1. **Install Backend Dependencies**:
```bash
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

2. **Set Up Environment Variables**:

Create or update your `.env` file in the project root:
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host/database

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
APP_NAME=Hackathon Todo API
DEBUG=True

# OpenAI Configuration (REQUIRED for agent)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

## Component 1: MCP Server

The MCP server exposes task management tools that can be used by MCP-compatible clients like Claude Desktop.

### Running the MCP Server

```bash
cd backend
python mcp_server.py
```

### Available MCP Tools

- `add_task(title, description?, due_date?)` - Add a new task
- `list_tasks(status?)` - List tasks, optionally filtered by status
- `update_task(id, title?, description?, due_date?)` - Update a task
- `delete_task(id)` - Delete a task
- `complete_task(id)` - Mark a task as completed

### Using with Claude Desktop

Add this to your Claude Desktop MCP configuration (usually at `~/Library/Application Support/Claude/claude_desktop_config.json` on Mac or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "hackathon-todo": {
      "command": "python",
      "args": ["C:/Users/HDD BANK/Desktop/final/hackathon-todo/backend/mcp_server.py"],
      "env": {
        "PYTHONPATH": "C:/Users/HDD BANK/Desktop/final/hackathon-todo/backend"
      }
    }
  }
}
```

Then restart Claude Desktop and you'll be able to ask Claude to manage your tasks!

## Component 2: OpenAI Agent

A standalone Python agent that uses OpenAI's function calling to manage tasks via natural language.

### Running the Agent

```bash
cd backend
python agent.py
```

This will run test conversations. You can also use it programmatically:

```python
from backend.agent import chat, simple_chat

# Simple one-shot interaction
response = simple_chat("Add a task to buy groceries")
print(response)

# With conversation history
result = chat("What are my tasks?", conversation_history=[])
print(result["message"])
# Continue the conversation
result = chat("Complete the first one", conversation_history=result["conversation_history"])
```

### Agent Capabilities

The agent understands natural language commands like:
- "Add a task to buy groceries tomorrow"
- "Show me all my tasks"
- "What tasks do I have pending?"
- "Complete the grocery task"
- "Delete the meeting task"
- "Update the presentation task to be due next Friday"

## Component 3: Chat API Endpoint

The FastAPI application now includes a `/chat` endpoint that provides RESTful access to the agent.

### Starting the API Server

```bash
# From the project root
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Using the Chat Endpoint

**Endpoint**: `POST /chat/`

**Request Body**:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_history": []
}
```

**Response**:
```json
{
  "message": "I've added a task called 'buy groceries' to your todo list!",
  "conversation_history": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "Add a task to buy groceries"},
    ...
  ]
}
```

### Example with cURL

```bash
# Add a task
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to prepare for the meeting tomorrow"
  }'

# List tasks
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What tasks do I have?"
  }'
```

### Example with Python

```python
import requests

url = "http://localhost:8000/chat/"

# Start a conversation
response = requests.post(url, json={
    "message": "Add a task to buy groceries"
})
result = response.json()
print(result["message"])

# Continue the conversation
response = requests.post(url, json={
    "message": "Show me all my tasks",
    "conversation_history": result["conversation_history"]
})
print(response.json()["message"])
```

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the integration tests:

```bash
python test_integration.py
```

This will test the basic task management functions. To test the full agent functionality, you'll need to set the `OPENAI_API_KEY` environment variable.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                 FastAPI App                      │
│  ┌───────────────────────────────────────────┐  │
│  │  /chat endpoint (app/routers/chat.py)     │  │
│  └─────────────────┬─────────────────────────┘  │
│                    │                             │
│  ┌─────────────────▼─────────────────────────┐  │
│  │  OpenAI Agent (backend/agent.py)          │  │
│  │  - Natural language processing             │  │
│  │  - Function calling                        │  │
│  └─────────────────┬─────────────────────────┘  │
│                    │                             │
│  ┌─────────────────▼─────────────────────────┐  │
│  │  Task Functions (backend/tasks.py)        │  │
│  │  - add_task, list_tasks, etc.             │  │
│  │  - File-based storage (tasks.json)        │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘

         ┌────────────────────────────┐
         │  MCP Server                 │
         │  (backend/mcp_server.py)    │
         │  - Standalone MCP interface │
         │  - Same task functions      │
         └────────────────────────────┘
```

## Task Storage

Currently, tasks are stored in `backend/tasks.json`. This is separate from the main application's PostgreSQL database.

**Future Enhancement**: Integrate with the main database by modifying `backend/tasks.py` to use SQLModel/SQLAlchemy instead of JSON file storage.

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you've set `OPENAI_API_KEY` in your `.env` file
- The `.env` file should be in the project root
- Restart your terminal/IDE after setting the variable

### "Module not found" errors
- Install all dependencies: `pip install -r requirements.txt && pip install -r backend/requirements.txt`
- Make sure you're in the correct directory when running commands

### MCP Server not working
- Check the MCP server logs for errors
- Verify the path in your MCP client configuration is correct
- Ensure Python is in your PATH

### Chat endpoint returns errors
- Check that the API server is running: `uvicorn app.main:app --reload`
- Verify your OPENAI_API_KEY is valid
- Check the server logs for detailed error messages

## Next Steps

1. **Frontend Integration**: Create a chat interface in the Next.js frontend
2. **Database Integration**: Connect the agent to the main PostgreSQL database
3. **Authentication**: Add JWT authentication to the chat endpoint
4. **Streaming**: Implement streaming responses for better UX
5. **Memory**: Add conversation persistence

## Resources

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Support

For issues and questions, please check:
- Backend README: `backend/README.md`
- Main README: `README.md`
- API Documentation: `http://localhost:8000/docs` (when server is running)
