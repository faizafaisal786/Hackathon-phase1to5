# Kafka + Dapr Event-Driven Architecture Specification

## Overview

This document specifies the event-driven architecture using Apache Kafka as the message broker and Dapr as the distributed application runtime for the hackathon-todo application.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Next.js)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND API (FastAPI)                              │
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │ Task CRUD   │    │ Auth        │    │ Chat        │                     │
│  │ Endpoints   │    │ Endpoints   │    │ Endpoints   │                     │
│  └──────┬──────┘    └─────────────┘    └─────────────┘                     │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────┐                                   │
│  │      Dapr Sidecar (daprd)           │                                   │
│  │  - Pub/Sub Component                │                                   │
│  │  - State Store Component            │                                   │
│  └──────┬──────────────────────────────┘                                   │
└─────────┼───────────────────────────────────────────────────────────────────┘
          │
          │ Publish Events
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         APACHE KAFKA CLUSTER                                 │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │  task-events    │  │  reminder-      │  │  notification-  │            │
│  │  topic          │  │  events topic   │  │  events topic   │            │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘            │
└───────────┼────────────────────┼────────────────────┼────────────────────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│  REMINDER SERVICE │  │  NOTIFICATION SVC │  │  ANALYTICS SVC    │
│                   │  │                   │  │  (Future)         │
│  Dapr Sidecar     │  │  Dapr Sidecar     │  │                   │
│  - Subscribe      │  │  - Subscribe      │  │                   │
│  - State Store    │  │  - Bindings       │  │                   │
│  - Cron Binding   │  │    (Email/Push)   │  │                   │
└───────────────────┘  └───────────────────┘  └───────────────────┘
```

---

## 1. Task Events Publishing

### Event Types

```python
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TaskEventType(str, Enum):
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
```

### Event Schema

```python
class TaskEvent(BaseModel):
    """Base event schema for all task-related events."""
    event_id: str                      # Unique event ID (UUID)
    event_type: TaskEventType          # Type of event
    event_time: datetime               # When event occurred
    event_version: str = "1.0"         # Schema version

    # Task data
    task_id: str                       # Task identifier
    user_id: str                       # Owner of the task

    # Event-specific payload
    payload: dict                      # Event-specific data

    # Metadata
    correlation_id: Optional[str]      # For tracing related events
    source: str = "backend-api"        # Service that emitted event

class TaskCreatedPayload(BaseModel):
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    priority: int = 0
    tags: List[str] = []
    is_recurring: bool = False
    recurrence_pattern: Optional[str]

class TaskCompletedPayload(BaseModel):
    completed_at: datetime
    was_overdue: bool
    time_to_complete_hours: Optional[float]  # Hours from creation to completion

class TaskDueDatePayload(BaseModel):
    old_due_date: Optional[datetime]
    new_due_date: Optional[datetime]
    reminder_before: int = 0           # Minutes before to remind
```

### Dapr Pub/Sub Component Configuration

```yaml
# components/pubsub-kafka.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskpubsub
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"              # Kafka broker address
    - name: consumerGroup
      value: "hackathon-todo"
    - name: clientID
      value: "backend-api"
    - name: authType
      value: "none"                    # Use "password" for SASL
    - name: maxMessageBytes
      value: "1048576"                 # 1MB max message size
    - name: consumeRetryInterval
      value: "100ms"
    - name: version
      value: "2.0.0"
```

### Backend Publisher Implementation

```python
# backend/events/publisher.py
import httpx
import uuid
from datetime import datetime
from typing import Optional
import os

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
PUBSUB_NAME = "taskpubsub"
TOPIC_NAME = "task-events"

async def publish_task_event(
    event_type: TaskEventType,
    task_id: str,
    user_id: str,
    payload: dict,
    correlation_id: Optional[str] = None
) -> bool:
    """Publish a task event to Kafka via Dapr."""

    event = TaskEvent(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        event_time=datetime.utcnow(),
        task_id=task_id,
        user_id=user_id,
        payload=payload,
        correlation_id=correlation_id or str(uuid.uuid4()),
        source="backend-api"
    )

    dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{PUBSUB_NAME}/{TOPIC_NAME}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                dapr_url,
                json=event.dict(),
                headers={
                    "Content-Type": "application/json",
                    "cloudevents-specversion": "1.0",
                    "cloudevents-type": event_type.value,
                    "cloudevents-source": "backend-api",
                    "cloudevents-id": event.event_id
                }
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Failed to publish event: {e}")
            return False
```

### Integration with Task Endpoints

```python
# backend/main.py - Updated endpoints

from events.publisher import publish_task_event, TaskEventType

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    new_task = add_task(task.dict())

    # Publish event
    await publish_task_event(
        event_type=TaskEventType.TASK_CREATED,
        task_id=new_task["id"],
        user_id=new_task.get("owner_id", "anonymous"),
        payload={
            "title": new_task["title"],
            "description": new_task.get("description"),
            "due_date": new_task.get("due_date"),
            "priority": new_task.get("priority", 0),
            "tags": new_task.get("tags", []),
            "is_recurring": new_task.get("is_recurring", False)
        }
    )

    return {"task": new_task}

@app.patch("/api/tasks/{task_id}/complete")
async def complete_task(task_id: str):
    task = mark_task_complete(task_id)

    # Calculate if overdue
    was_overdue = False
    if task.get("due_date"):
        was_overdue = datetime.fromisoformat(task["due_date"]) < datetime.utcnow()

    # Publish event
    await publish_task_event(
        event_type=TaskEventType.TASK_COMPLETED,
        task_id=task_id,
        user_id=task.get("owner_id", "anonymous"),
        payload={
            "completed_at": datetime.utcnow().isoformat(),
            "was_overdue": was_overdue
        }
    )

    return {"task": task}
```

### Kafka Topics Configuration

```yaml
# kafka/topics.yaml
topics:
  - name: task-events
    partitions: 3
    replication-factor: 1
    config:
      retention.ms: 604800000          # 7 days retention
      cleanup.policy: delete
      max.message.bytes: 1048576

  - name: reminder-events
    partitions: 2
    replication-factor: 1
    config:
      retention.ms: 86400000           # 1 day retention
      cleanup.policy: delete

  - name: notification-events
    partitions: 2
    replication-factor: 1
    config:
      retention.ms: 86400000           # 1 day retention
      cleanup.policy: delete

  - name: dead-letter-queue
    partitions: 1
    replication-factor: 1
    config:
      retention.ms: 2592000000         # 30 days retention
```

---

## 2. Reminder Service

### Service Overview

The Reminder Service is responsible for:
- Scheduling reminders based on task due dates
- Checking for upcoming due tasks periodically
- Publishing reminder events when tasks are due soon
- Managing reminder state (sent/pending)

### Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    REMINDER SERVICE                          │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Event        │    │ Scheduler    │    │ Reminder     │  │
│  │ Subscriber   │    │ (Cron)       │    │ Publisher    │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Reminder State Store                    │   │
│  │  (Redis via Dapr State Management)                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Data Models

```python
# reminder-service/models.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ReminderStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    CANCELLED = "cancelled"
    FAILED = "failed"

class Reminder(BaseModel):
    """Reminder record stored in state store."""
    id: str                            # Unique reminder ID
    task_id: str                       # Associated task
    user_id: str                       # User to remind

    # Timing
    remind_at: datetime                # When to send reminder
    due_date: datetime                 # Task due date
    reminder_before: int               # Minutes before (15, 30, 60, 1440)

    # Task context
    task_title: str
    task_priority: int

    # Status
    status: ReminderStatus = ReminderStatus.PENDING
    sent_at: Optional[datetime] = None
    created_at: datetime

class ReminderEvent(BaseModel):
    """Event published when reminder should be sent."""
    event_id: str
    event_type: str = "reminder.triggered"
    event_time: datetime

    reminder_id: str
    task_id: str
    user_id: str
    task_title: str
    task_priority: int
    due_date: datetime
    minutes_until_due: int

    # Notification preferences
    channels: list[str] = ["push", "email"]  # Notification channels
```

### Dapr Components

```yaml
# reminder-service/components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminderstore
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis:6379"
    - name: redisPassword
      value: ""
    - name: actorStateStore
      value: "true"
```

```yaml
# reminder-service/components/cron-binding.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "*/1 * * * *"             # Every minute
    - name: direction
      value: "input"
```

```yaml
# reminder-service/components/subscription.yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-events-subscription
spec:
  topic: task-events
  route: /events/task
  pubsubname: taskpubsub
  deadLetterTopic: dead-letter-queue
```

### Service Implementation

```python
# reminder-service/main.py
from fastapi import FastAPI
from datetime import datetime, timedelta
import httpx
import uuid

app = FastAPI(title="Reminder Service")

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
STATE_STORE = "reminderstore"
PUBSUB_NAME = "taskpubsub"

# ============================================================
# Event Subscriber - Listen for task events
# ============================================================

@app.post("/events/task")
async def handle_task_event(event: dict):
    """Handle incoming task events from Kafka."""
    event_type = event.get("event_type")

    if event_type == "task.created":
        await handle_task_created(event)
    elif event_type == "task.due_date.set":
        await handle_due_date_set(event)
    elif event_type == "task.due_date.changed":
        await handle_due_date_changed(event)
    elif event_type == "task.completed":
        await handle_task_completed(event)
    elif event_type == "task.deleted":
        await handle_task_deleted(event)

    return {"status": "processed"}

async def handle_task_created(event: dict):
    """Create reminder when task with due date is created."""
    payload = event.get("payload", {})
    due_date = payload.get("due_date")
    reminder_before = payload.get("reminder_before", 0)

    if not due_date or reminder_before == 0:
        return  # No reminder needed

    await create_reminder(
        task_id=event["task_id"],
        user_id=event["user_id"],
        task_title=payload["title"],
        task_priority=payload.get("priority", 0),
        due_date=datetime.fromisoformat(due_date),
        reminder_before=reminder_before
    )

async def handle_task_completed(event: dict):
    """Cancel reminders when task is completed."""
    task_id = event["task_id"]
    await cancel_reminders_for_task(task_id)

async def handle_task_deleted(event: dict):
    """Cancel reminders when task is deleted."""
    task_id = event["task_id"]
    await cancel_reminders_for_task(task_id)

# ============================================================
# Reminder Management
# ============================================================

async def create_reminder(
    task_id: str,
    user_id: str,
    task_title: str,
    task_priority: int,
    due_date: datetime,
    reminder_before: int
) -> Reminder:
    """Create and store a new reminder."""

    remind_at = due_date - timedelta(minutes=reminder_before)

    # Don't create reminders for past times
    if remind_at <= datetime.utcnow():
        return None

    reminder = Reminder(
        id=str(uuid.uuid4()),
        task_id=task_id,
        user_id=user_id,
        remind_at=remind_at,
        due_date=due_date,
        reminder_before=reminder_before,
        task_title=task_title,
        task_priority=task_priority,
        status=ReminderStatus.PENDING,
        created_at=datetime.utcnow()
    )

    # Save to state store
    await save_reminder(reminder)

    # Add to user's reminder index
    await add_to_reminder_index(user_id, reminder.id)

    return reminder

async def save_reminder(reminder: Reminder):
    """Save reminder to Dapr state store."""
    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/{STATE_STORE}",
            json=[{
                "key": f"reminder:{reminder.id}",
                "value": reminder.dict()
            }]
        )

async def cancel_reminders_for_task(task_id: str):
    """Cancel all pending reminders for a task."""
    # Query reminders by task_id and mark as cancelled
    reminders = await get_reminders_by_task(task_id)
    for reminder in reminders:
        if reminder.status == ReminderStatus.PENDING:
            reminder.status = ReminderStatus.CANCELLED
            await save_reminder(reminder)

# ============================================================
# Cron Job - Check for due reminders
# ============================================================

@app.post("/reminder-cron")
async def check_reminders():
    """Cron job that runs every minute to check for due reminders."""

    now = datetime.utcnow()
    window_end = now + timedelta(minutes=1)

    # Get all pending reminders due in the next minute
    pending_reminders = await get_pending_reminders(now, window_end)

    for reminder in pending_reminders:
        await trigger_reminder(reminder)

    return {"processed": len(pending_reminders)}

async def trigger_reminder(reminder: Reminder):
    """Publish reminder event and update status."""

    minutes_until_due = int(
        (reminder.due_date - datetime.utcnow()).total_seconds() / 60
    )

    event = ReminderEvent(
        event_id=str(uuid.uuid4()),
        event_time=datetime.utcnow(),
        reminder_id=reminder.id,
        task_id=reminder.task_id,
        user_id=reminder.user_id,
        task_title=reminder.task_title,
        task_priority=reminder.task_priority,
        due_date=reminder.due_date,
        minutes_until_due=max(0, minutes_until_due),
        channels=["push", "email"]
    )

    # Publish to notification topic
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{PUBSUB_NAME}/reminder-events",
            json=event.dict()
        )

    if response.status_code == 204:
        reminder.status = ReminderStatus.SENT
        reminder.sent_at = datetime.utcnow()
    else:
        reminder.status = ReminderStatus.FAILED

    await save_reminder(reminder)

# ============================================================
# Query Helpers
# ============================================================

async def get_pending_reminders(start: datetime, end: datetime) -> list[Reminder]:
    """Query reminders due between start and end time."""
    # In production, use Dapr query API or dedicated index
    # This is a simplified version
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:{DAPR_HTTP_PORT}/v1.0-alpha1/state/{STATE_STORE}/query",
            json={
                "filter": {
                    "AND": [
                        {"EQ": {"status": "pending"}},
                        {"GTE": {"remind_at": start.isoformat()}},
                        {"LTE": {"remind_at": end.isoformat()}}
                    ]
                }
            }
        )
        results = response.json().get("results", [])
        return [Reminder(**r["data"]) for r in results]
```

### Reminder Service Dockerfile

```dockerfile
# reminder-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

## 3. Notification Service

### Service Overview

The Notification Service is responsible for:
- Receiving reminder events and other notification triggers
- Sending notifications via multiple channels (email, push, in-app)
- Managing user notification preferences
- Tracking notification delivery status

### Notification Channels

```python
# notification-service/models.py
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NotificationChannel(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    IN_APP = "in_app"
    SMS = "sms"                        # Future
    WEBHOOK = "webhook"                # Future

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"

class NotificationType(str, Enum):
    TASK_REMINDER = "task_reminder"
    TASK_OVERDUE = "task_overdue"
    TASK_ASSIGNED = "task_assigned"
    DAILY_DIGEST = "daily_digest"
    WEEKLY_SUMMARY = "weekly_summary"

class Notification(BaseModel):
    id: str
    user_id: str
    type: NotificationType

    # Content
    title: str
    body: str
    data: dict = {}                    # Additional payload (task_id, etc.)

    # Delivery
    channels: List[NotificationChannel]
    channel_status: dict[str, NotificationStatus] = {}

    # Timing
    created_at: datetime
    sent_at: Optional[datetime]
    read_at: Optional[datetime]

class UserNotificationPreferences(BaseModel):
    user_id: str

    # Channel preferences
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True

    # Type preferences
    reminder_notifications: bool = True
    overdue_notifications: bool = True
    digest_notifications: bool = True

    # Quiet hours
    quiet_hours_enabled: bool = False
    quiet_hours_start: str = "22:00"   # HH:MM format
    quiet_hours_end: str = "08:00"

    # Email address
    email: Optional[str]

    # Push token (FCM/APNS)
    push_tokens: List[str] = []
```

### Dapr Components

```yaml
# notification-service/components/subscription.yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: reminder-events-subscription
spec:
  topic: reminder-events
  route: /events/reminder
  pubsubname: taskpubsub

---
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: notification-events-subscription
spec:
  topic: notification-events
  route: /events/notification
  pubsubname: taskpubsub
```

```yaml
# notification-service/components/email-binding.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: email-sender
spec:
  type: bindings.smtp
  version: v1
  metadata:
    - name: host
      value: "smtp.sendgrid.net"
    - name: port
      value: "587"
    - name: user
      secretKeyRef:
        name: smtp-secrets
        key: username
    - name: password
      secretKeyRef:
        name: smtp-secrets
        key: password
    - name: skipTLSVerify
      value: "false"
```

```yaml
# notification-service/components/push-binding.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: push-sender
spec:
  type: bindings.http
  version: v1
  metadata:
    - name: url
      value: "https://fcm.googleapis.com/fcm/send"
    - name: method
      value: "POST"
```

### Service Implementation

```python
# notification-service/main.py
from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
import httpx
import uuid

app = FastAPI(title="Notification Service")

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
STATE_STORE = "notificationstore"

# ============================================================
# Event Handlers
# ============================================================

@app.post("/events/reminder")
async def handle_reminder_event(event: dict, background_tasks: BackgroundTasks):
    """Handle reminder events from Reminder Service."""

    notification = await create_notification_from_reminder(event)
    background_tasks.add_task(send_notification, notification)

    return {"status": "accepted", "notification_id": notification.id}

async def create_notification_from_reminder(event: dict) -> Notification:
    """Create notification record from reminder event."""

    user_id = event["user_id"]
    prefs = await get_user_preferences(user_id)

    # Determine channels based on preferences
    channels = []
    if prefs.email_enabled and prefs.reminder_notifications:
        channels.append(NotificationChannel.EMAIL)
    if prefs.push_enabled and prefs.reminder_notifications:
        channels.append(NotificationChannel.PUSH)
    if prefs.in_app_enabled:
        channels.append(NotificationChannel.IN_APP)

    # Check quiet hours
    if prefs.quiet_hours_enabled and is_quiet_hours(prefs):
        channels = [NotificationChannel.IN_APP]  # Only in-app during quiet hours

    minutes = event["minutes_until_due"]
    time_text = format_time_until(minutes)

    notification = Notification(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type=NotificationType.TASK_REMINDER,
        title=f"Task Due {time_text}",
        body=f"'{event['task_title']}' is due {time_text}",
        data={
            "task_id": event["task_id"],
            "due_date": event["due_date"],
            "priority": event["task_priority"]
        },
        channels=channels,
        channel_status={ch.value: NotificationStatus.PENDING for ch in channels},
        created_at=datetime.utcnow()
    )

    await save_notification(notification)
    return notification

# ============================================================
# Notification Sending
# ============================================================

async def send_notification(notification: Notification):
    """Send notification through all configured channels."""

    for channel in notification.channels:
        try:
            if channel == NotificationChannel.EMAIL:
                await send_email_notification(notification)
            elif channel == NotificationChannel.PUSH:
                await send_push_notification(notification)
            elif channel == NotificationChannel.IN_APP:
                await send_in_app_notification(notification)

            notification.channel_status[channel.value] = NotificationStatus.SENT
        except Exception as e:
            print(f"Failed to send {channel} notification: {e}")
            notification.channel_status[channel.value] = NotificationStatus.FAILED

    notification.sent_at = datetime.utcnow()
    await save_notification(notification)

async def send_email_notification(notification: Notification):
    """Send email via Dapr SMTP binding."""

    prefs = await get_user_preferences(notification.user_id)
    if not prefs.email:
        return

    email_body = render_email_template(notification)

    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://localhost:{DAPR_HTTP_PORT}/v1.0/bindings/email-sender",
            json={
                "operation": "create",
                "metadata": {
                    "emailTo": prefs.email,
                    "emailFrom": "reminders@hackathon-todo.app",
                    "subject": notification.title
                },
                "data": email_body
            }
        )

async def send_push_notification(notification: Notification):
    """Send push notification via FCM."""

    prefs = await get_user_preferences(notification.user_id)
    if not prefs.push_tokens:
        return

    for token in prefs.push_tokens:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"http://localhost:{DAPR_HTTP_PORT}/v1.0/bindings/push-sender",
                json={
                    "operation": "create",
                    "data": {
                        "to": token,
                        "notification": {
                            "title": notification.title,
                            "body": notification.body
                        },
                        "data": notification.data
                    }
                },
                headers={
                    "Authorization": f"key={os.getenv('FCM_SERVER_KEY')}"
                }
            )

async def send_in_app_notification(notification: Notification):
    """Store notification for in-app display."""
    # Already stored, just add to user's notification feed
    await add_to_user_feed(notification.user_id, notification.id)

# ============================================================
# User Notification Feed API
# ============================================================

@app.get("/api/notifications/{user_id}")
async def get_user_notifications(
    user_id: str,
    unread_only: bool = False,
    limit: int = 20
):
    """Get notifications for a user."""
    notifications = await get_notifications_for_user(user_id, unread_only, limit)
    unread_count = await get_unread_count(user_id)

    return {
        "notifications": notifications,
        "unread_count": unread_count
    }

@app.patch("/api/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str):
    """Mark a notification as read."""
    notification = await get_notification(notification_id)
    notification.read_at = datetime.utcnow()
    notification.channel_status[NotificationChannel.IN_APP.value] = NotificationStatus.READ
    await save_notification(notification)
    return {"status": "ok"}

@app.post("/api/notifications/{user_id}/mark-all-read")
async def mark_all_read(user_id: str):
    """Mark all notifications as read for a user."""
    await mark_all_notifications_read(user_id)
    return {"status": "ok"}

# ============================================================
# Preferences API
# ============================================================

@app.get("/api/notifications/{user_id}/preferences")
async def get_preferences(user_id: str):
    """Get user notification preferences."""
    prefs = await get_user_preferences(user_id)
    return prefs

@app.put("/api/notifications/{user_id}/preferences")
async def update_preferences(user_id: str, prefs: UserNotificationPreferences):
    """Update user notification preferences."""
    prefs.user_id = user_id
    await save_user_preferences(prefs)
    return prefs

@app.post("/api/notifications/{user_id}/push-token")
async def register_push_token(user_id: str, token: str):
    """Register a push notification token."""
    prefs = await get_user_preferences(user_id)
    if token not in prefs.push_tokens:
        prefs.push_tokens.append(token)
        await save_user_preferences(prefs)
    return {"status": "registered"}

# ============================================================
# Helper Functions
# ============================================================

def format_time_until(minutes: int) -> str:
    if minutes <= 0:
        return "now"
    elif minutes < 60:
        return f"in {minutes} minutes"
    elif minutes < 1440:
        hours = minutes // 60
        return f"in {hours} hour{'s' if hours > 1 else ''}"
    else:
        days = minutes // 1440
        return f"in {days} day{'s' if days > 1 else ''}"

def is_quiet_hours(prefs: UserNotificationPreferences) -> bool:
    """Check if current time is within quiet hours."""
    now = datetime.now().strftime("%H:%M")
    start = prefs.quiet_hours_start
    end = prefs.quiet_hours_end

    if start <= end:
        return start <= now <= end
    else:  # Crosses midnight
        return now >= start or now <= end

def render_email_template(notification: Notification) -> str:
    """Render HTML email template."""
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #333;">{notification.title}</h2>
        <p style="color: #666; font-size: 16px;">{notification.body}</p>
        <a href="https://hackathon-todo.app/tasks/{notification.data.get('task_id')}"
           style="background: #3B82F6; color: white; padding: 10px 20px;
                  text-decoration: none; border-radius: 5px; display: inline-block;">
            View Task
        </a>
        <p style="color: #999; font-size: 12px; margin-top: 30px;">
            You received this email because you have reminder notifications enabled.
            <a href="https://hackathon-todo.app/settings/notifications">Manage preferences</a>
        </p>
    </body>
    </html>
    """
```

### Notification Service Dockerfile

```dockerfile
# notification-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
```

---

## 4. Docker Compose Setup

```yaml
# docker-compose.kafka.yaml
version: '3.8'

services:
  # ============================================================
  # Infrastructure
  # ============================================================

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  # ============================================================
  # Backend API with Dapr
  # ============================================================

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DAPR_HTTP_PORT=3500
    depends_on:
      - kafka
      - redis

  backend-dapr:
    image: daprio/daprd:1.12.0
    command: [
      "./daprd",
      "-app-id", "backend",
      "-app-port", "8000",
      "-dapr-http-port", "3500",
      "-components-path", "/components"
    ]
    volumes:
      - ./components:/components
    network_mode: "service:backend"
    depends_on:
      - backend

  # ============================================================
  # Reminder Service with Dapr
  # ============================================================

  reminder-service:
    build: ./reminder-service
    ports:
      - "8001:8001"
    environment:
      - DAPR_HTTP_PORT=3501
    depends_on:
      - kafka
      - redis

  reminder-dapr:
    image: daprio/daprd:1.12.0
    command: [
      "./daprd",
      "-app-id", "reminder-service",
      "-app-port", "8001",
      "-dapr-http-port", "3501",
      "-components-path", "/components"
    ]
    volumes:
      - ./reminder-service/components:/components
    network_mode: "service:reminder-service"
    depends_on:
      - reminder-service

  # ============================================================
  # Notification Service with Dapr
  # ============================================================

  notification-service:
    build: ./notification-service
    ports:
      - "8002:8002"
    environment:
      - DAPR_HTTP_PORT=3502
      - FCM_SERVER_KEY=${FCM_SERVER_KEY}
    depends_on:
      - kafka
      - redis

  notification-dapr:
    image: daprio/daprd:1.12.0
    command: [
      "./daprd",
      "-app-id", "notification-service",
      "-app-port", "8002",
      "-dapr-http-port", "3502",
      "-components-path", "/components"
    ]
    volumes:
      - ./notification-service/components:/components
    network_mode: "service:notification-service"
    depends_on:
      - notification-service

  # ============================================================
  # Frontend
  # ============================================================

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend

volumes:
  redis-data:
```

---

## 5. Event Flow Diagrams

### Task Creation with Reminder

```
User                Frontend           Backend            Kafka              Reminder Svc        Notification Svc
 │                    │                  │                  │                    │                    │
 │ Create Task        │                  │                  │                    │                    │
 │ (due: tomorrow,    │                  │                  │                    │                    │
 │  remind: 1hr)      │                  │                  │                    │                    │
 │───────────────────>│                  │                  │                    │                    │
 │                    │  POST /api/tasks │                  │                    │                    │
 │                    │─────────────────>│                  │                    │                    │
 │                    │                  │                  │                    │                    │
 │                    │                  │ Publish          │                    │                    │
 │                    │                  │ task.created     │                    │                    │
 │                    │                  │─────────────────>│                    │                    │
 │                    │                  │                  │                    │                    │
 │                    │   201 Created    │                  │ Deliver event      │                    │
 │                    │<─────────────────│                  │───────────────────>│                    │
 │                    │                  │                  │                    │                    │
 │   Task Created     │                  │                  │                    │ Create Reminder    │
 │<───────────────────│                  │                  │                    │ (remind_at =       │
 │                    │                  │                  │                    │  due - 1hr)        │
 │                    │                  │                  │                    │────────┐           │
 │                    │                  │                  │                    │        │           │
 │                    │                  │                  │                    │<───────┘           │
 │                    │                  │                  │                    │                    │
 ═══════════════════════════════════════════════════════════════════════════════════════════════════════
                                    ... 23 hours later (1hr before due) ...
 ═══════════════════════════════════════════════════════════════════════════════════════════════════════
 │                    │                  │                  │                    │                    │
 │                    │                  │                  │    Cron triggers   │                    │
 │                    │                  │                  │<───────────────────│                    │
 │                    │                  │                  │                    │                    │
 │                    │                  │                  │                    │ Check pending      │
 │                    │                  │                  │                    │ reminders          │
 │                    │                  │                  │                    │────────┐           │
 │                    │                  │                  │                    │        │           │
 │                    │                  │                  │                    │<───────┘           │
 │                    │                  │                  │                    │                    │
 │                    │                  │                  │ Publish            │                    │
 │                    │                  │                  │ reminder.triggered │                    │
 │                    │                  │                  │<───────────────────│                    │
 │                    │                  │                  │                    │                    │
 │                    │                  │                  │ Deliver event      │                    │
 │                    │                  │                  │────────────────────────────────────────>│
 │                    │                  │                  │                    │                    │
 │                    │                  │                  │                    │                    │ Send Email
 │                    │                  │                  │                    │                    │────────┐
 │  Email: "Task due  │                  │                  │                    │                    │        │
 │  in 1 hour"        │                  │                  │                    │                    │<───────┘
 │<═══════════════════════════════════════════════════════════════════════════════════════════════════│
 │                    │                  │                  │                    │                    │
 │                    │                  │                  │                    │                    │ Send Push
 │  Push Notification │                  │                  │                    │                    │────────┐
 │<═══════════════════════════════════════════════════════════════════════════════════════════════════│        │
 │                    │                  │                  │                    │                    │<───────┘
```

---

## 6. Monitoring & Observability

### Metrics to Track

```yaml
# Prometheus metrics
metrics:
  - name: task_events_published_total
    type: counter
    labels: [event_type, status]

  - name: task_events_consumed_total
    type: counter
    labels: [event_type, service, status]

  - name: reminder_processing_duration_seconds
    type: histogram
    labels: [status]

  - name: notification_send_duration_seconds
    type: histogram
    labels: [channel, status]

  - name: notification_delivery_total
    type: counter
    labels: [channel, status, type]

  - name: kafka_consumer_lag
    type: gauge
    labels: [topic, consumer_group]
```

### Health Checks

```python
# Each service should expose health endpoints

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/health/ready")
async def readiness():
    # Check dependencies
    kafka_ok = await check_kafka_connection()
    redis_ok = await check_redis_connection()

    if kafka_ok and redis_ok:
        return {"status": "ready"}

    return JSONResponse(
        status_code=503,
        content={"status": "not ready", "kafka": kafka_ok, "redis": redis_ok}
    )
```

---

## 7. Error Handling & Retry

### Dead Letter Queue

```python
# Handle failed events
@app.post("/events/dead-letter")
async def handle_dead_letter(event: dict):
    """Process events that failed multiple times."""

    # Log for investigation
    logger.error(f"Dead letter event: {event}")

    # Store for manual review
    await store_failed_event(event)

    # Alert on-call if critical
    if event.get("event_type") in ["task.created", "reminder.triggered"]:
        await send_alert("Critical event failed", event)

    return {"status": "logged"}
```

### Retry Configuration

```yaml
# Dapr retry policy
apiVersion: dapr.io/v1alpha1
kind: Resiliency
metadata:
  name: myresiliency
spec:
  policies:
    retries:
      pubsubRetry:
        policy: constant
        maxRetries: 3
        duration: 5s

    timeouts:
      general: 30s

    circuitBreakers:
      pubsubCB:
        maxRequests: 1
        interval: 60s
        timeout: 30s
        trip: consecutiveFailures >= 5

  targets:
    components:
      taskpubsub:
        outbound:
          retry: pubsubRetry
          circuitBreaker: pubsubCB
```
