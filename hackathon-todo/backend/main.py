"""FastAPI Backend with Kafka Event Publishing via Dapr."""

from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent import simple_chat, chat
from tasks import (
    add_task, list_tasks, update_task, delete_task,
    complete_task, uncomplete_task, load_tasks, get_task_by_id
)
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
from typing import Optional, List
import logging

# Event publishing
from events import TaskEventType, publish_task_event

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Todo App Backend",
    description="Task management API with AI and event-driven architecture",
    version="2.0.0"
)

# Enhanced CORS configuration for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


# ============================================================
# Models
# ============================================================

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    due_date: str = ""
    priority: int = 0
    tags: List[str] = []
    reminder_before: int = 0  # Minutes before due date to remind


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[int] = None
    tags: Optional[List[str]] = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    conversation_history: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


# ============================================================
# Task Endpoints with Event Publishing
# ============================================================

@app.get("/api/tasks")
async def get_tasks(
    status: Optional[str] = None,
    priority: Optional[int] = None,
    tags: Optional[str] = None
):
    """Get all tasks with optional filtering."""
    tasks_data = load_tasks()

    # Apply filters
    if status:
        tasks_data = [t for t in tasks_data if t.get("status") == status]
    if priority is not None:
        tasks_data = [t for t in tasks_data if t.get("priority", 0) >= priority]
    if tags:
        tag_list = tags.split(",")
        tasks_data = [
            t for t in tasks_data
            if any(tag in t.get("tags", []) for tag in tag_list)
        ]

    return {"tasks": tasks_data}


@app.post("/api/tasks")
async def create_task(task: TaskCreate, background_tasks: BackgroundTasks):
    """Create a new task and publish task.created event."""
    task_data = add_task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority,
        tags=task.tags,
        reminder_before=task.reminder_before
    )

    # Publish event in background
    background_tasks.add_task(
        publish_task_event,
        event_type=TaskEventType.TASK_CREATED,
        task_id=task_data["id"],
        payload={
            "title": task_data["title"],
            "description": task_data.get("description", ""),
            "due_date": task_data.get("due_date"),
            "priority": task_data.get("priority", 0),
            "tags": task_data.get("tags", []),
            "reminder_before": task_data.get("reminder_before", 0)
        }
    )

    logger.info(f"Task created: {task_data['id']}")
    return task_data


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """Get a specific task by ID."""
    task = get_task_by_id(task_id)
    if task:
        return task
    return JSONResponse(status_code=404, content={"error": "Task not found"})


@app.put("/api/tasks/{task_id}")
async def update_task_endpoint(
    task_id: str,
    task: TaskUpdate,
    background_tasks: BackgroundTasks
):
    """Update a task and publish task.updated event."""
    # Get original task for comparison
    original_task = get_task_by_id(task_id)
    if not original_task:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    # Track changes
    changes = {}

    # Apply updates
    update_data = {}
    if task.title is not None:
        update_data["title"] = task.title
        if task.title != original_task.get("title"):
            changes["title"] = {"old": original_task.get("title"), "new": task.title}
    if task.description is not None:
        update_data["description"] = task.description
        if task.description != original_task.get("description"):
            changes["description"] = {"old": original_task.get("description"), "new": task.description}
    if task.due_date is not None:
        update_data["due_date"] = task.due_date
        old_due = original_task.get("due_date")
        if task.due_date != old_due:
            changes["due_date"] = {"old": old_due, "new": task.due_date}
    if task.priority is not None:
        update_data["priority"] = task.priority
        if task.priority != original_task.get("priority", 0):
            changes["priority"] = {"old": original_task.get("priority", 0), "new": task.priority}
    if task.tags is not None:
        update_data["tags"] = task.tags
        if task.tags != original_task.get("tags", []):
            changes["tags"] = {"old": original_task.get("tags", []), "new": task.tags}

    updated_task = update_task(task_id, **update_data)

    if updated_task and changes:
        # Publish task.updated event
        background_tasks.add_task(
            publish_task_event,
            event_type=TaskEventType.TASK_UPDATED,
            task_id=task_id,
            payload={"changes": changes}
        )

        # Publish specific events for due date and priority changes
        if "due_date" in changes:
            event_type = (
                TaskEventType.TASK_DUE_DATE_SET
                if not changes["due_date"]["old"]
                else TaskEventType.TASK_DUE_DATE_CHANGED
            )
            background_tasks.add_task(
                publish_task_event,
                event_type=event_type,
                task_id=task_id,
                payload={
                    "old_due_date": changes["due_date"]["old"],
                    "new_due_date": changes["due_date"]["new"],
                    "reminder_before": updated_task.get("reminder_before", 0)
                }
            )

        if "priority" in changes:
            background_tasks.add_task(
                publish_task_event,
                event_type=TaskEventType.TASK_PRIORITY_CHANGED,
                task_id=task_id,
                payload={
                    "old_priority": changes["priority"]["old"],
                    "new_priority": changes["priority"]["new"]
                }
            )

        logger.info(f"Task updated: {task_id}, changes: {list(changes.keys())}")

    return updated_task or JSONResponse(
        status_code=404,
        content={"error": "Task not found"}
    )


@app.delete("/api/tasks/{task_id}")
async def delete_task_endpoint(task_id: str, background_tasks: BackgroundTasks):
    """Delete a task and publish task.deleted event."""
    task = get_task_by_id(task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    result = delete_task(task_id)

    # Publish event
    background_tasks.add_task(
        publish_task_event,
        event_type=TaskEventType.TASK_DELETED,
        task_id=task_id,
        payload={
            "title": task.get("title", ""),
            "was_completed": task.get("status") == "completed"
        }
    )

    logger.info(f"Task deleted: {task_id}")
    return {"message": result, "task_id": task_id}


@app.patch("/api/tasks/{task_id}/complete")
async def complete_task_endpoint(task_id: str, background_tasks: BackgroundTasks):
    """Mark a task as complete and publish task.completed event."""
    task = get_task_by_id(task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    # Check if already completed
    if task.get("status") == "completed":
        return task

    # Calculate if overdue
    was_overdue = False
    time_to_complete = None
    if task.get("due_date"):
        try:
            due = datetime.fromisoformat(task["due_date"].replace("Z", "+00:00"))
            was_overdue = due < datetime.now(due.tzinfo) if due.tzinfo else due < datetime.now()
        except (ValueError, TypeError):
            pass

    if task.get("created_at"):
        try:
            created = datetime.fromisoformat(task["created_at"].replace("Z", "+00:00"))
            time_to_complete = (datetime.now() - created.replace(tzinfo=None)).total_seconds() / 3600
        except (ValueError, TypeError):
            pass

    result = complete_task(task_id)
    updated_task = get_task_by_id(task_id)

    # Publish event
    background_tasks.add_task(
        publish_task_event,
        event_type=TaskEventType.TASK_COMPLETED,
        task_id=task_id,
        payload={
            "completed_at": datetime.utcnow().isoformat(),
            "was_overdue": was_overdue,
            "time_to_complete_hours": time_to_complete
        }
    )

    logger.info(f"Task completed: {task_id}, was_overdue: {was_overdue}")
    return updated_task or {"message": result}


@app.patch("/api/tasks/{task_id}/uncomplete")
async def uncomplete_task_endpoint(task_id: str, background_tasks: BackgroundTasks):
    """Mark a task as not complete and publish task.uncompleted event."""
    task = get_task_by_id(task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    if task.get("status") != "completed":
        return task

    result = uncomplete_task(task_id)
    updated_task = get_task_by_id(task_id)

    # Publish event
    background_tasks.add_task(
        publish_task_event,
        event_type=TaskEventType.TASK_UNCOMPLETED,
        task_id=task_id,
        payload={"uncompleted_at": datetime.utcnow().isoformat()}
    )

    logger.info(f"Task uncompleted: {task_id}")
    return updated_task or {"message": result}


# ============================================================
# Dapr Event Subscriber Endpoint
# ============================================================

@app.post("/events/task")
async def handle_task_event(event: dict):
    """
    Handle incoming task events from Dapr pub/sub.
    This endpoint is called by Dapr when events are published to task-events topic.
    """
    event_type = event.get("type") or event.get("data", {}).get("event_type")
    task_id = event.get("data", {}).get("task_id")

    logger.info(f"Received event: {event_type} for task {task_id}")

    # Events are processed here if needed (e.g., for audit logging)
    # Most processing is done by dedicated services (reminder-service, etc.)

    return {"status": "processed"}


# ============================================================
# Chat Endpoints
# ============================================================

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat with AI agent."""
    conversation_id = request.conversation_id or str(uuid.uuid4())

    conversation_history = []
    if request.conversation_history:
        for msg in request.conversation_history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                conversation_history.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

    result = chat(request.message, conversation_history if conversation_history else None)

    from conversations import save_message
    save_message(conversation_id, "user", request.message)
    save_message(conversation_id, "assistant", result["message"])

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


@app.post("/chat/")
async def chat_endpoint_alt(request: ChatRequest):
    """Chat endpoint (alternative path)."""
    return await chat_endpoint(request)


@app.get("/chat/conversations")
async def get_conversations():
    """Get all conversations."""
    return []


@app.get("/chat/conversations/{conversation_id}")
async def get_conversation_endpoint(conversation_id: str):
    """Get a specific conversation."""
    from conversations import get_conversation as get_conv_from_db
    messages = get_conv_from_db(conversation_id)
    return {
        "id": conversation_id,
        "messages": [{"role": role, "content": content} for role, content in messages]
    }


@app.delete("/chat/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    return {"message": "Conversation deleted"}


# ============================================================
# Auth Endpoints (Stub)
# ============================================================

@app.post("/auth/register")
async def register(request: RegisterRequest):
    """Register a new user (stub endpoint)."""
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
    """Login endpoint (stub)."""
    return {
        "access_token": f"dummy_token_{uuid.uuid4()}",
        "token_type": "bearer"
    }


# ============================================================
# Health & Info Endpoints
# ============================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Todo App Backend with AI and Event-Driven Architecture",
        "version": "2.0.0",
        "endpoints": [
            "/api/tasks",
            "/api/chat",
            "/chat/",
            "/auth/register",
            "/auth/token",
            "/health"
        ],
        "features": [
            "Kafka event publishing via Dapr",
            "Task CRUD with events",
            "AI chat integration"
        ]
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/health/ready")
async def readiness():
    """Readiness check endpoint."""
    return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
