"""Task management with in-memory storage."""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

# In-memory storage for Vercel serverless deployment
# Note: Tasks will be lost on function cold starts
# For production, use a proper database (PostgreSQL, MongoDB, etc.)
tasks: List[Dict[str, Any]] = []


def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from in-memory storage."""
    return tasks


def save_tasks() -> None:
    """Save tasks (no-op for in-memory storage)."""
    pass


def get_task_by_id(task_id: str) -> Optional[Dict[str, Any]]:
    """Get a task by its ID."""
    for task in tasks:
        if task["id"] == task_id:
            return task.copy()
    return None


def add_task(
    title: str,
    description: str = "",
    due_date: str = "",
    priority: int = 0,
    tags: Optional[List[str]] = None,
    reminder_before: int = 0
) -> Dict[str, Any]:
    """
    Add a new task.

    Args:
        title: Task title
        description: Task description
        due_date: Due date (ISO format string)
        priority: Priority level (0=none, 1=low, 2=medium, 3=high, 4=urgent)
        tags: List of tag names
        reminder_before: Minutes before due date to send reminder

    Returns:
        The created task object
    """
    global tasks

    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "due_date": due_date if due_date else None,
        "status": "pending",
        "priority": priority,
        "tags": tags or [],
        "reminder_before": reminder_before,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

    tasks.append(task)
    save_tasks()

    return task


def list_tasks(status: str = "") -> str:
    """List tasks with optional status filter (returns formatted string)."""
    filtered = tasks
    if status:
        filtered = [t for t in filtered if t["status"] == status]

    if not filtered:
        return "No tasks found."

    result = []
    for t in filtered:
        priority_str = ["", "Low", "Medium", "High", "Urgent"][t.get("priority", 0)]
        result.append(
            f"- {t['title']} (ID: {t['id']}, Status: {t['status']}"
            f"{f', Priority: {priority_str}' if priority_str else ''})"
        )
        if t.get("description"):
            result.append(f"  Description: {t['description']}")
        if t.get("due_date"):
            result.append(f"  Due: {t['due_date']}")
        if t.get("tags"):
            result.append(f"  Tags: {', '.join(t['tags'])}")

    return "\n".join(result)


def update_task(
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: Optional[int] = None,
    tags: Optional[List[str]] = None,
    reminder_before: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """
    Update a task.

    Args:
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)
        due_date: New due date (optional)
        priority: New priority (optional)
        tags: New tags list (optional)
        reminder_before: New reminder setting (optional)

    Returns:
        Updated task object or None if not found
    """
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title
            if description is not None:
                task["description"] = description
            if due_date is not None:
                task["due_date"] = due_date if due_date else None
            if priority is not None:
                task["priority"] = priority
            if tags is not None:
                task["tags"] = tags
            if reminder_before is not None:
                task["reminder_before"] = reminder_before

            task["updated_at"] = datetime.utcnow().isoformat()
            save_tasks()
            return task.copy()

    return None


def delete_task(task_id: str) -> str:
    """Delete a task by ID."""
    global tasks

    original_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) < original_len:
        save_tasks()
        return f"Task {task_id} deleted"

    return "Task not found"


def complete_task(task_id: str) -> str:
    """Mark a task as completed."""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
            task["completed_at"] = datetime.utcnow().isoformat()
            task["updated_at"] = datetime.utcnow().isoformat()
            save_tasks()
            return f"Task {task_id} marked as completed"

    return "Task not found"


def uncomplete_task(task_id: str) -> str:
    """Mark a task as not completed (pending)."""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "pending"
            task.pop("completed_at", None)
            task["updated_at"] = datetime.utcnow().isoformat()
            save_tasks()
            return f"Task {task_id} marked as pending"

    return "Task not found"


def get_tasks_by_status(status: str) -> List[Dict[str, Any]]:
    """Get all tasks with a specific status."""
    return [t.copy() for t in tasks if t.get("status") == status]


def get_tasks_with_due_date() -> List[Dict[str, Any]]:
    """Get all tasks that have a due date set."""
    return [t.copy() for t in tasks if t.get("due_date")]


def get_overdue_tasks() -> List[Dict[str, Any]]:
    """Get all tasks that are past their due date."""
    now = datetime.utcnow()
    overdue = []

    for task in tasks:
        if task.get("due_date") and task.get("status") != "completed":
            try:
                due = datetime.fromisoformat(task["due_date"].replace("Z", "+00:00"))
                if due.replace(tzinfo=None) < now:
                    overdue.append(task.copy())
            except (ValueError, TypeError):
                pass

    return overdue


def get_tasks_by_priority(min_priority: int = 1) -> List[Dict[str, Any]]:
    """Get all tasks with priority >= min_priority."""
    return [
        t.copy() for t in tasks
        if t.get("priority", 0) >= min_priority
    ]


def get_tasks_by_tags(tag_list: List[str], match_all: bool = False) -> List[Dict[str, Any]]:
    """
    Get tasks matching specified tags.

    Args:
        tag_list: List of tags to match
        match_all: If True, task must have ALL tags; if False, ANY tag

    Returns:
        List of matching tasks
    """
    result = []
    for task in tasks:
        task_tags = set(task.get("tags", []))
        search_tags = set(tag_list)

        if match_all:
            if search_tags.issubset(task_tags):
                result.append(task.copy())
        else:
            if search_tags & task_tags:
                result.append(task.copy())

    return result
