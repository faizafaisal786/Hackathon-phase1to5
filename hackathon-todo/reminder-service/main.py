"""
Reminder Service - Event-driven reminder scheduling with cron job.

This service:
1. Subscribes to task events (task.created, task.due_date.set, etc.)
2. Creates/updates reminders based on task due dates
3. Runs a cron job to check for due reminders
4. Publishes reminder events to trigger notifications
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from models import Reminder, ReminderStatus, ReminderEvent, TaskEventData
from state_store import (
    save_reminder,
    get_reminder,
    get_pending_reminders,
    cancel_reminders_for_task,
    add_to_task_index
)
from upstash_kafka import publish_reminder_event, get_kafka

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3501")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "taskpubsub")
REMINDER_TOPIC = os.getenv("REMINDER_TOPIC", "reminder-events")
CRON_INTERVAL_SECONDS = int(os.getenv("CRON_INTERVAL_SECONDS", "60"))

BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"

# Scheduler instance
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - start/stop scheduler."""
    # Start the scheduler
    scheduler.add_job(
        check_and_trigger_reminders,
        trigger=IntervalTrigger(seconds=CRON_INTERVAL_SECONDS),
        id="reminder_cron",
        name="Check and trigger due reminders",
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"Reminder cron started (interval: {CRON_INTERVAL_SECONDS}s)")

    yield

    # Shutdown scheduler
    scheduler.shutdown()
    logger.info("Reminder cron stopped")


app = FastAPI(
    title="Reminder Service",
    description="Event-driven reminder scheduling service",
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================
# Dapr Pub/Sub Event Handlers
# ============================================================

@app.post("/events/task")
async def handle_task_event(event: dict, background_tasks: BackgroundTasks):
    """
    Handle incoming task events from Kafka via Dapr.

    Supported events:
    - task.created: Create reminder if due date is set
    - task.due_date.set: Create new reminder
    - task.due_date.changed: Update existing reminder
    - task.completed: Cancel pending reminders
    - task.deleted: Cancel pending reminders
    """
    # Extract event data (CloudEvents format)
    event_type = event.get("type", "")
    data = event.get("data", {})

    task_id = data.get("task_id", "")
    user_id = data.get("user_id", "anonymous")
    payload = data.get("payload", {})

    logger.info(f"Received event: {event_type} for task {task_id}")

    if event_type == "task.created":
        await handle_task_created(task_id, user_id, payload)

    elif event_type in ("task.due_date.set", "task.due_date.changed"):
        await handle_due_date_change(task_id, user_id, payload)

    elif event_type in ("task.completed", "task.deleted"):
        await handle_task_completed_or_deleted(task_id)

    return {"status": "processed"}


async def handle_task_created(task_id: str, user_id: str, payload: dict):
    """Handle task.created event - create reminder if due date exists."""
    due_date_str = payload.get("due_date")
    reminder_before = payload.get("reminder_before", 0)

    if not due_date_str or reminder_before <= 0:
        logger.debug(f"No reminder needed for task {task_id}")
        return

    await create_reminder(
        task_id=task_id,
        user_id=user_id,
        task_title=payload.get("title", "Untitled Task"),
        task_priority=payload.get("priority", 0),
        due_date_str=due_date_str,
        reminder_before=reminder_before
    )


async def handle_due_date_change(task_id: str, user_id: str, payload: dict):
    """Handle due date set/changed - update or create reminder."""
    new_due_date = payload.get("new_due_date")
    reminder_before = payload.get("reminder_before", 0)

    # Cancel existing reminders for this task
    await cancel_reminders_for_task(task_id)

    if not new_due_date or reminder_before <= 0:
        return

    # Create new reminder with updated due date
    await create_reminder(
        task_id=task_id,
        user_id=user_id,
        task_title=payload.get("title", "Task"),
        task_priority=payload.get("priority", 0),
        due_date_str=new_due_date,
        reminder_before=reminder_before
    )


async def handle_task_completed_or_deleted(task_id: str):
    """Handle task completion/deletion - cancel all reminders."""
    cancelled = await cancel_reminders_for_task(task_id)
    logger.info(f"Cancelled {cancelled} reminders for completed/deleted task {task_id}")


# ============================================================
# Reminder Management
# ============================================================

async def create_reminder(
    task_id: str,
    user_id: str,
    task_title: str,
    task_priority: int,
    due_date_str: str,
    reminder_before: int
) -> Optional[Reminder]:
    """Create a new reminder for a task."""
    try:
        # Parse due date
        due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
        due_date = due_date.replace(tzinfo=None)  # Work with naive datetime

        # Calculate reminder time
        remind_at = due_date - timedelta(minutes=reminder_before)

        # Don't create reminders for past times
        if remind_at <= datetime.utcnow():
            logger.info(f"Reminder time already passed for task {task_id}")
            return None

        reminder = Reminder(
            task_id=task_id,
            user_id=user_id,
            remind_at=remind_at,
            due_date=due_date,
            reminder_before=reminder_before,
            task_title=task_title,
            task_priority=task_priority,
            status=ReminderStatus.PENDING
        )

        await save_reminder(reminder)
        await add_to_task_index(task_id, reminder.id)

        logger.info(
            f"Created reminder {reminder.id} for task {task_id}, "
            f"will trigger at {remind_at.isoformat()}"
        )

        return reminder

    except (ValueError, TypeError) as e:
        logger.error(f"Failed to create reminder for task {task_id}: {e}")
        return None


# ============================================================
# Cron Job - Check and Trigger Reminders
# ============================================================

async def check_and_trigger_reminders():
    """
    Cron job that runs periodically to check for due reminders.
    This is the main reminder processing loop.
    """
    now = datetime.utcnow()
    logger.debug(f"Checking reminders at {now.isoformat()}")

    pending_reminders = await get_pending_reminders()
    triggered_count = 0

    for reminder in pending_reminders:
        # Check if reminder is due
        if reminder.remind_at <= now:
            success = await trigger_reminder(reminder)
            if success:
                triggered_count += 1

    if triggered_count > 0:
        logger.info(f"Triggered {triggered_count} reminders")


async def trigger_reminder(reminder: Reminder) -> bool:
    """Trigger a reminder by publishing a reminder event."""
    now = datetime.utcnow()

    # Calculate minutes until due
    minutes_until_due = int(
        (reminder.due_date - now).total_seconds() / 60
    )
    minutes_until_due = max(0, minutes_until_due)

    # Try Upstash Kafka first (FREE), then Dapr
    kafka = get_kafka()

    if kafka.enabled:
        # Use FREE Upstash Kafka
        success = await publish_reminder_event(
            reminder_id=reminder.id,
            task_id=reminder.task_id,
            user_id=reminder.user_id,
            task_title=reminder.task_title,
            due_date=reminder.due_date.isoformat(),
            minutes_until_due=minutes_until_due,
            task_priority=reminder.task_priority
        )

        if success:
            reminder.status = ReminderStatus.SENT
            reminder.sent_at = now
            await save_reminder(reminder)
            logger.info(f"Triggered reminder {reminder.id} via Upstash (FREE)")
            return True

    # Fallback to Dapr if Upstash not available
    try:
        event = ReminderEvent(
            reminder_id=reminder.id,
            task_id=reminder.task_id,
            user_id=reminder.user_id,
            task_title=reminder.task_title,
            task_priority=reminder.task_priority,
            due_date=reminder.due_date.isoformat(),
            minutes_until_due=minutes_until_due,
            channels=["push", "email", "in_app"]
        )

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{BASE_URL}/v1.0/publish/{PUBSUB_NAME}/{REMINDER_TOPIC}",
                json=event.model_dump(mode="json"),
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in (200, 204):
                reminder.status = ReminderStatus.SENT
                reminder.sent_at = now
                await save_reminder(reminder)
                logger.info(f"Triggered reminder {reminder.id} via Dapr")
                return True

    except httpx.ConnectError:
        pass
    except Exception as e:
        logger.error(f"Error triggering reminder: {e}")

    # Mark as sent to avoid repeated triggers
    reminder.status = ReminderStatus.SENT
    reminder.sent_at = now
    await save_reminder(reminder)
    logger.info(f"Reminder {reminder.id} marked as sent (local)")
    return True


# ============================================================
# Manual Trigger Endpoint (for Dapr cron binding)
# ============================================================

@app.post("/reminder-cron")
async def manual_cron_trigger():
    """
    Manual trigger endpoint for Dapr cron binding.
    Can be used instead of APScheduler in Dapr environments.
    """
    await check_and_trigger_reminders()
    return {"status": "processed", "timestamp": datetime.utcnow().isoformat()}


# ============================================================
# Health & Info Endpoints
# ============================================================

@app.get("/")
async def root():
    """Root endpoint with service info."""
    return {
        "service": "Reminder Service",
        "version": "1.0.0",
        "status": "running",
        "cron_interval": f"{CRON_INTERVAL_SECONDS}s"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "scheduler_running": scheduler.running,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health/ready")
async def readiness():
    """Readiness check endpoint."""
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================
# Debug Endpoints (Development Only)
# ============================================================

@app.get("/debug/reminders")
async def list_all_reminders():
    """List all reminders (for debugging)."""
    reminders = await get_pending_reminders()
    return {
        "count": len(reminders),
        "reminders": [r.model_dump(mode="json") for r in reminders]
    }


@app.post("/debug/trigger")
async def force_trigger():
    """Force trigger reminder check (for debugging)."""
    await check_and_trigger_reminders()
    return {"status": "triggered"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
