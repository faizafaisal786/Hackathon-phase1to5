"""
Phase 1: CLI to Web API Converter for Deployment
Converts the CLI task manager into a web API for cloud deployment
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# Import the TaskManager from the original CLI app
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import Task as CLITask, TaskManager

app = FastAPI(
    title="Task Manager API - Phase 1",
    description="Simple task management API converted from CLI app",
    version="1.0.0"
)

# Initialize task manager
task_manager = TaskManager()

# Pydantic models for API
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Task Manager API - Phase 1",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "tasks": "/tasks",
            "health": "/health"
        }
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "task-manager-phase1"}

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    """Create a new task"""
    new_task = task_manager.add_task(task.title, task.description)
    return TaskResponse(
        id=new_task.id,
        title=new_task.title,
        description=new_task.description,
        completed=new_task.completed
    )

@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks():
    """List all tasks"""
    tasks = task_manager.list_tasks()
    return [
        TaskResponse(
            id=t.id,
            title=t.title,
            description=t.description,
            completed=t.completed
        )
        for t in tasks
    ]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Get a specific task"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed
    )

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    success = task_manager.update_task(
        task_id,
        task_update.title,
        task_update.description
    )

    if not success:
        raise HTTPException(status_code=400, detail="Failed to update task")

    updated_task = task_manager.get_task(task_id)
    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed
    )

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    success = task_manager.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete task")

    return {"message": f"Task {task_id} deleted successfully"}

@app.patch("/tasks/{task_id}/complete")
def mark_complete(task_id: int):
    """Mark a task as complete"""
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.completed:
        return {"message": "Task already completed"}

    success = task_manager.mark_complete(task_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to mark task complete")

    return {"message": f"Task {task_id} marked as complete"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
