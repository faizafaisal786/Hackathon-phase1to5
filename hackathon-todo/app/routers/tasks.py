"""
Task CRUD routes (all protected by JWT authentication).
"""
from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task, TaskCreate, TaskUpdate, TaskResponse, User
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Create a new task.

    Requires JWT authentication. The task will be owned by the authenticated user.
    """
    db_task = Task(
        **task_data.model_dump(),
        owner_id=current_user.id
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)],
    completed: bool = None
):
    """
    List all tasks for the authenticated user.

    Requires JWT authentication. Returns only tasks owned by the current user.
    Optionally filter by completion status.
    """
    statement = select(Task).where(Task.owner_id == current_user.id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    tasks = session.exec(statement).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Get a specific task by ID.

    Requires JWT authentication. Users can only access their own tasks.
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Ensure user owns the task
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Update a task.

    Requires JWT authentication. Users can only update their own tasks.
    All fields are optional - only provided fields will be updated.
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Ensure user owns the task
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Delete a task.

    Requires JWT authentication. Users can only delete their own tasks.
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Ensure user owns the task
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    session.delete(task)
    session.commit()

    return None


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_complete(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Mark a task as complete.

    Requires JWT authentication. Users can only mark their own tasks.
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Ensure user owns the task
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    task.completed = True
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch("/{task_id}/incomplete", response_model=TaskResponse)
async def mark_task_incomplete(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Mark a task as incomplete.

    Requires JWT authentication. Users can only mark their own tasks.
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Ensure user owns the task
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    task.completed = False
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
