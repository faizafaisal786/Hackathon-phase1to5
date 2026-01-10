import json
import uuid
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

tasks = load_tasks()

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(title: str, description: str = "", due_date: str = "") -> str:
    global tasks
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks()
    return f"Task '{title}' added with ID {task_id}"

def list_tasks(status: str = "") -> str:
    filtered = tasks
    if status:
        filtered = [t for t in filtered if t["status"] == status]
    if not filtered:
        return "No tasks found."
    result = []
    for t in filtered:
        result.append(f"- {t['title']} (ID: {t['id']}, Status: {t['status']})")
        if t['description']:
            result.append(f"  Description: {t['description']}")
        if t['due_date']:
            result.append(f"  Due: {t['due_date']}")
    return "\n".join(result)

def update_task(task_id: str, title: str = "", description: str = "", due_date: str = "") -> str:
    for t in tasks:
        if t["id"] == task_id:
            if title:
                t["title"] = title
            if description:
                t["description"] = description
            if due_date:
                t["due_date"] = due_date
            save_tasks()
            return f"Task {task_id} updated"
    return "Task not found"

def delete_task(task_id: str) -> str:
    global tasks
    original_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) < original_len:
        save_tasks()
        return f"Task {task_id} deleted"
    return "Task not found"

def complete_task(task_id: str) -> str:
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "completed"
            save_tasks()
            return f"Task {task_id} marked as completed"
    return "Task not found"