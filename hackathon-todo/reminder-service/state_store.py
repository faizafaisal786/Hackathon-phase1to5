"""State store operations via Dapr."""

import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

import httpx

from models import Reminder, ReminderStatus

logger = logging.getLogger(__name__)

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3501")
STATE_STORE_NAME = os.getenv("STATE_STORE_NAME", "statestore")
BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"

# In-memory fallback when Dapr is not available
_local_reminders: Dict[str, Reminder] = {}
_task_reminder_index: Dict[str, List[str]] = {}  # task_id -> [reminder_ids]


async def save_reminder(reminder: Reminder) -> bool:
    """Save a reminder to the state store."""
    reminder.updated_at = datetime.utcnow()

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{BASE_URL}/v1.0/state/{STATE_STORE_NAME}",
                json=[{
                    "key": f"reminder:{reminder.id}",
                    "value": reminder.model_dump(mode="json")
                }]
            )

            if response.status_code in (200, 204):
                logger.debug(f"Saved reminder {reminder.id} to state store")
                return True
            else:
                logger.error(f"Failed to save reminder: {response.status_code}")

    except httpx.ConnectError:
        logger.warning("Dapr not available, using local storage")

    # Fallback to local storage
    _local_reminders[reminder.id] = reminder
    return True


async def get_reminder(reminder_id: str) -> Optional[Reminder]:
    """Get a reminder by ID."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{BASE_URL}/v1.0/state/{STATE_STORE_NAME}/reminder:{reminder_id}"
            )

            if response.status_code == 200:
                data = response.json()
                if data:
                    return Reminder(**data)
            return None

    except httpx.ConnectError:
        logger.warning("Dapr not available, using local storage")

    # Fallback to local storage
    return _local_reminders.get(reminder_id)


async def delete_reminder(reminder_id: str) -> bool:
    """Delete a reminder from state store."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.delete(
                f"{BASE_URL}/v1.0/state/{STATE_STORE_NAME}/reminder:{reminder_id}"
            )
            if response.status_code in (200, 204):
                return True

    except httpx.ConnectError:
        pass

    # Fallback to local storage
    if reminder_id in _local_reminders:
        del _local_reminders[reminder_id]
        return True
    return False


async def add_to_task_index(task_id: str, reminder_id: str) -> None:
    """Add a reminder to the task index."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Get existing index
            response = await client.get(
                f"{BASE_URL}/v1.0/state/{STATE_STORE_NAME}/task_reminders:{task_id}"
            )

            reminder_ids = []
            if response.status_code == 200 and response.json():
                reminder_ids = response.json()

            if reminder_id not in reminder_ids:
                reminder_ids.append(reminder_id)

            # Save updated index
            await client.post(
                f"{BASE_URL}/v1.0/state/{STATE_STORE_NAME}",
                json=[{
                    "key": f"task_reminders:{task_id}",
                    "value": reminder_ids
                }]
            )
            return

    except httpx.ConnectError:
        pass

    # Fallback to local storage
    if task_id not in _task_reminder_index:
        _task_reminder_index[task_id] = []
    if reminder_id not in _task_reminder_index[task_id]:
        _task_reminder_index[task_id].append(reminder_id)


async def get_reminders_for_task(task_id: str) -> List[Reminder]:
    """Get all reminders for a task."""
    reminders = []

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{BASE_URL}/v1.0/state/{STATE_STORE_NAME}/task_reminders:{task_id}"
            )

            if response.status_code == 200 and response.json():
                reminder_ids = response.json()
                for rid in reminder_ids:
                    reminder = await get_reminder(rid)
                    if reminder:
                        reminders.append(reminder)
                return reminders

    except httpx.ConnectError:
        pass

    # Fallback to local storage
    reminder_ids = _task_reminder_index.get(task_id, [])
    for rid in reminder_ids:
        if rid in _local_reminders:
            reminders.append(_local_reminders[rid])

    return reminders


async def get_pending_reminders() -> List[Reminder]:
    """Get all pending reminders (for cron job processing)."""
    pending = []

    # Check local storage first
    for reminder in _local_reminders.values():
        if reminder.status == ReminderStatus.PENDING:
            pending.append(reminder)

    # If Dapr is available, we would query by status
    # For now, local storage is the primary source during cron checks

    return pending


async def cancel_reminders_for_task(task_id: str) -> int:
    """Cancel all pending reminders for a task."""
    cancelled_count = 0
    reminders = await get_reminders_for_task(task_id)

    for reminder in reminders:
        if reminder.status == ReminderStatus.PENDING:
            reminder.status = ReminderStatus.CANCELLED
            reminder.updated_at = datetime.utcnow()
            await save_reminder(reminder)
            cancelled_count += 1

    logger.info(f"Cancelled {cancelled_count} reminders for task {task_id}")
    return cancelled_count
