"""Event publisher for Dapr pub/sub with Kafka."""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

from .models import TaskEventType, TaskEvent

logger = logging.getLogger(__name__)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "taskpubsub")
TASK_EVENTS_TOPIC = os.getenv("TASK_EVENTS_TOPIC", "task-events")
REMINDER_EVENTS_TOPIC = os.getenv("REMINDER_EVENTS_TOPIC", "reminder-events")

# Feature flag for enabling/disabling event publishing
EVENTS_ENABLED = os.getenv("EVENTS_ENABLED", "true").lower() == "true"


class EventPublisher:
    """Publishes events to Kafka via Dapr sidecar."""

    def __init__(
        self,
        dapr_port: str = DAPR_HTTP_PORT,
        pubsub_name: str = PUBSUB_NAME,
        enabled: bool = EVENTS_ENABLED
    ):
        self.dapr_port = dapr_port
        self.pubsub_name = pubsub_name
        self.enabled = enabled and HTTPX_AVAILABLE
        self.base_url = f"http://localhost:{dapr_port}"

    async def publish(
        self,
        topic: str,
        event: TaskEvent
    ) -> bool:
        """Publish an event to a Kafka topic via Dapr."""
        if not self.enabled:
            logger.debug(f"Event publishing disabled, skipping: {event.event_type}")
            return True

        url = f"{self.base_url}/v1.0/publish/{self.pubsub_name}/{topic}"

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    url,
                    json=event.to_cloudevents_dict(),
                    headers={
                        "Content-Type": "application/cloudevents+json",
                    }
                )

                if response.status_code in (200, 204):
                    logger.info(
                        f"Published event: {event.event_type} "
                        f"for task {event.task_id}"
                    )
                    return True
                else:
                    logger.error(
                        f"Failed to publish event: {response.status_code} "
                        f"{response.text}"
                    )
                    return False

        except httpx.ConnectError:
            logger.warning(
                f"Dapr sidecar not available at {self.base_url}, "
                f"event not published: {event.event_type}"
            )
            return False
        except Exception as e:
            logger.error(f"Error publishing event: {e}")
            return False

    async def publish_task_event(
        self,
        event_type: TaskEventType,
        task_id: str,
        user_id: str = "anonymous",
        payload: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None
    ) -> bool:
        """Convenience method to publish a task event."""
        event = TaskEvent(
            event_type=event_type,
            task_id=task_id,
            user_id=user_id,
            payload=payload or {},
            correlation_id=correlation_id or str(uuid.uuid4())
        )
        return await self.publish(TASK_EVENTS_TOPIC, event)


# Global publisher instance
_publisher: Optional[EventPublisher] = None


def get_publisher() -> EventPublisher:
    """Get or create the global event publisher."""
    global _publisher
    if _publisher is None:
        _publisher = EventPublisher()
    return _publisher


async def publish_task_event(
    event_type: TaskEventType,
    task_id: str,
    user_id: str = "anonymous",
    payload: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None
) -> bool:
    """
    Publish a task event to Kafka via Dapr.

    This is the main function to use for publishing events from endpoints.

    Args:
        event_type: Type of task event (TaskEventType enum)
        task_id: ID of the task
        user_id: ID of the user (defaults to "anonymous")
        payload: Event-specific data
        correlation_id: Optional ID for tracing related events

    Returns:
        True if event was published successfully (or publishing is disabled)
    """
    publisher = get_publisher()
    return await publisher.publish_task_event(
        event_type=event_type,
        task_id=task_id,
        user_id=user_id,
        payload=payload,
        correlation_id=correlation_id
    )


async def publish_reminder_event(
    reminder_id: str,
    task_id: str,
    user_id: str,
    task_title: str,
    due_date: str,
    minutes_until_due: int,
    task_priority: int = 0,
    channels: Optional[list] = None
) -> bool:
    """
    Publish a reminder event to trigger notifications.

    Args:
        reminder_id: ID of the reminder
        task_id: ID of the associated task
        user_id: ID of the user to notify
        task_title: Title of the task
        due_date: Due date of the task (ISO format)
        minutes_until_due: Minutes until the task is due
        task_priority: Priority level of the task
        channels: Notification channels to use

    Returns:
        True if event was published successfully
    """
    from .models import ReminderEvent

    publisher = get_publisher()

    if not publisher.enabled:
        logger.debug("Event publishing disabled, skipping reminder event")
        return True

    event_data = ReminderEvent(
        reminder_id=reminder_id,
        task_id=task_id,
        user_id=user_id,
        task_title=task_title,
        task_priority=task_priority,
        due_date=due_date,
        minutes_until_due=minutes_until_due,
        channels=channels or ["push", "email", "in_app"]
    )

    url = f"{publisher.base_url}/v1.0/publish/{publisher.pubsub_name}/{REMINDER_EVENTS_TOPIC}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                url,
                json=event_data.model_dump(),
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in (200, 204):
                logger.info(f"Published reminder event for task {task_id}")
                return True
            else:
                logger.error(f"Failed to publish reminder: {response.status_code}")
                return False

    except Exception as e:
        logger.error(f"Error publishing reminder event: {e}")
        return False
