"""Data models for the Reminder Service."""

from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid


class ReminderStatus(str, Enum):
    """Status of a reminder."""
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"
    FAILED = "failed"


class Reminder(BaseModel):
    """Reminder record stored in state store."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str
    user_id: str = "anonymous"

    # Timing
    remind_at: datetime
    due_date: datetime
    reminder_before: int  # Minutes before due date

    # Task context
    task_title: str
    task_priority: int = 0

    # Status tracking
    status: ReminderStatus = ReminderStatus.PENDING
    sent_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ReminderEvent(BaseModel):
    """Event published when a reminder is triggered."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "reminder.triggered"
    event_time: datetime = Field(default_factory=datetime.utcnow)

    reminder_id: str
    task_id: str
    user_id: str
    task_title: str
    task_priority: int = 0
    due_date: str
    minutes_until_due: int

    channels: List[str] = Field(default_factory=lambda: ["push", "email", "in_app"])

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TaskEventData(BaseModel):
    """Data received from task events."""
    task_id: str
    user_id: str = "anonymous"
    payload: dict = Field(default_factory=dict)
    correlation_id: Optional[str] = None
