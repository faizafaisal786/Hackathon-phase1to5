from fastapi import FastAPI, Form
from pydantic import BaseModel
from agent import simple_chat, chat
from tasks import add_task, list_tasks, update_task, delete_task, complete_task, load_tasks
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
from typing import Optional, List

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth models
class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Task models
class TaskCreate(BaseModel):
    title: str
    description: str = ""
    due_date: str = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None

# Chat models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    conversation_history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# Task endpoints
@app.get("/api/tasks")
async def get_tasks():
    """Get all tasks"""
    tasks_data = load_tasks()
    return {"tasks": tasks_data}

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    """Create a new task"""
    result = add_task(task.title, task.description, task.due_date)
    tasks_data = load_tasks()
    # Return the last added task
    if tasks_data:
        return tasks_data[-1]
    return {"message": result}

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """Get a specific task by ID"""
    tasks_data = load_tasks()
    for task in tasks_data:
        if task["id"] == task_id:
            return task
    return {"error": "Task not found"}

@app.put("/api/tasks/{task_id}")
async def update_task_endpoint(task_id: str, task: TaskUpdate):
    """Update a task"""
    title = task.title if task.title else ""
    description = task.description if task.description else ""
    due_date = task.due_date if task.due_date else ""
    result = update_task(task_id, title, description, due_date)
    tasks_data = load_tasks()
    for t in tasks_data:
        if t["id"] == task_id:
            return t
    return {"message": result}

@app.delete("/api/tasks/{task_id}")
async def delete_task_endpoint(task_id: str):
    """Delete a task"""
    result = delete_task(task_id)
    return {"message": result}

@app.patch("/api/tasks/{task_id}/complete")
async def complete_task_endpoint(task_id: str):
    """Mark a task as complete"""
    result = complete_task(task_id)
    tasks_data = load_tasks()
    for t in tasks_data:
        if t["id"] == task_id:
            return t
    return {"message": result}

# Chat endpoint (compatible with frontend expectations)
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat with AI agent"""
    # Generate conversation ID if not provided
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    # Convert conversation_history to the format expected by agent
    conversation_history = []
    if request.conversation_history:
        for msg in request.conversation_history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                conversation_history.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
    
    # Get response from agent
    result = chat(request.message, conversation_history if conversation_history else None)
    
    # Save conversation messages
    from conversations import save_message
    save_message(conversation_id, "user", request.message)
    save_message(conversation_id, "assistant", result["message"])
    
    # Convert conversation history to the format expected by frontend
    frontend_history = []
    if "conversation_history" in result:
        for msg in result["conversation_history"]:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                frontend_history.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
    
    return {
        "message": result["message"],
        "conversation_id": conversation_id,
        "conversation_history": frontend_history
    }

# Alternative chat endpoint path (for frontend compatibility)
@app.post("/chat/")
async def chat_endpoint_alt(request: ChatRequest):
    """Chat endpoint (alternative path)"""
    return await chat_endpoint(request)

# Conversation management endpoints (stub for frontend compatibility)
@app.get("/chat/conversations")
async def get_conversations():
    """Get all conversations (stub endpoint)"""
    return []

@app.get("/chat/conversations/{conversation_id}")
async def get_conversation_endpoint(conversation_id: str):
    """Get a specific conversation (stub endpoint)"""
    from conversations import get_conversation as get_conv_from_db
    messages = get_conv_from_db(conversation_id)
    return {
        "id": conversation_id,
        "messages": [{"role": role, "content": content} for role, content in messages]
    }

@app.delete("/chat/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation (stub endpoint)"""
    return {"message": "Conversation deleted"}

# Auth endpoints (stub for frontend compatibility - Phase 3)
@app.post("/auth/register")
async def register(request: RegisterRequest):
    """Register a new user (stub endpoint for Phase 3)"""
    # In Phase 3, we accept any registration
    return {
        "id": 1,
        "email": request.email,
        "username": request.username,
        "full_name": request.full_name,
        "is_active": True,
        "created_at": datetime.now().isoformat()
    }

@app.post("/auth/token")
async def login(username: str = Form(...), password: str = Form(...)):
    """Login endpoint (stub for Phase 3) - accepts form data"""
    # In Phase 3, we accept any login and return a dummy token
    # For production, this should use proper authentication
    return {
        "access_token": f"dummy_token_{uuid.uuid4()}",
        "token_type": "bearer"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Todo App Backend with AI", "endpoints": ["/api/tasks", "/api/chat", "/chat/", "/auth/register", "/auth/token"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)