"""Event models for Kafka pub/sub via Dapr."""

from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid


class TaskEventType(str, Enum):
    """Task event types published to Kafka."""
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_DELETED = "task.deleted"
    TASK_COMPLETED = "task.completed"
    TASK_UNCOMPLETED = "task.uncompleted"
    TASK_DUE_DATE_SET = "task.due_date.set"
    TASK_DUE_DATE_CHANGED = "task.due_date.changed"
    TASK_PRIORITY_CHANGED = "task.priority.changed"
    TASK_TAGS_UPDATED = "task.tags.updated"
    TASK_RECURRING_GENERATED = "task.recurring.generated"


class TaskEvent(BaseModel):
    """Base event schema for all task-related events (CloudEvents compatible)."""

    # CloudEvents required fields
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: TaskEventType
    event_time: datetime = Field(default_factory=datetime.utcnow)
    event_version: str = "1.0"

    # Task identification
    task_id: str
    user_id: str = "anonymous"

    # Event payload
    payload: Dict[str, Any] = Field(default_factory=dict)

    # Tracing
    correlation_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str = "backend-api"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def to_cloudevents_dict(self) -> Dict[str, Any]:
        """Convert to CloudEvents format."""
        return {
            "specversion": "1.0",
            "type": self.event_type.value,
            "source": self.source,
            "id": self.event_id,
            "time": self.event_time.isoformat(),
            "datacontenttype": "application/json",
            "data": {
                "event_version": self.event_version,
                "task_id": self.task_id,
                "user_id": self.user_id,
                "payload": self.payload,
                "correlation_id": self.correlation_id
            }
        }


class TaskCreatedPayload(BaseModel):
    """Payload for task.created event."""
    title: str
    description: Optional[str] = ""
    due_date: Optional[str] = None
    priority: int = 0
    tags: List[str] = Field(default_factory=list)
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    reminder_before: int = 0


class TaskUpdatedPayload(BaseModel):
    """Payload for task.updated event."""
    changes: Dict[str, Any]  # {field: {"old": value, "new": value}}


class TaskCompletedPayload(BaseModel):
    """Payload for task.completed event."""
    completed_at: datetime
    was_overdue: bool = False
    time_to_complete_hours: Optional[float] = None


class TaskDeletedPayload(BaseModel):
    """Payload for task.deleted event."""
    title: str
    was_completed: bool


class TaskDueDatePayload(BaseModel):
    """Payload for due date events."""
    old_due_date: Optional[str] = None
    new_due_date: Optional[str] = None
    reminder_before: int = 0


class ReminderEvent(BaseModel):
    """Event published when a reminder should be triggered."""
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
