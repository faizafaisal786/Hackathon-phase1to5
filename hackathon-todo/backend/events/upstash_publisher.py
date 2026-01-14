"""
Upstash Kafka Publisher - FREE tier compatible.
Upstash provides REST API for Kafka which works without Dapr sidecar.
"""

import os
import logging
import base64
import json
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

# Upstash Kafka Configuration
UPSTASH_KAFKA_URL = os.getenv("UPSTASH_KAFKA_URL", "")
UPSTASH_KAFKA_USERNAME = os.getenv("UPSTASH_KAFKA_USERNAME", "")
UPSTASH_KAFKA_PASSWORD = os.getenv("UPSTASH_KAFKA_PASSWORD", "")

# Feature flag
EVENTS_ENABLED = os.getenv("EVENTS_ENABLED", "true").lower() == "true"


class UpstashKafkaPublisher:
    """
    Publishes events to Upstash Kafka via REST API.
    Works without Dapr - perfect for serverless/free deployments.
    """

    def __init__(self):
        self.base_url = UPSTASH_KAFKA_URL
        self.username = UPSTASH_KAFKA_USERNAME
        self.password = UPSTASH_KAFKA_PASSWORD
        self.enabled = bool(self.base_url and self.username and EVENTS_ENABLED and HTTPX_AVAILABLE)

        if self.enabled:
            # Create basic auth header
            credentials = f"{self.username}:{self.password}"
            self.auth_header = base64.b64encode(credentials.encode()).decode()
            logger.info("Upstash Kafka publisher initialized")
        else:
            logger.warning("Upstash Kafka not configured, events will be logged locally")

    async def publish(self, topic: str, event: TaskEvent) -> bool:
        """Publish an event to Upstash Kafka."""
        if not self.enabled:
            logger.debug(f"[LOCAL] Event: {event.event_type} for task {event.task_id}")
            return True

        try:
            # Upstash Kafka REST API endpoint
            url = f"{self.base_url}/produce/{topic}"

            payload = {
                "value": json.dumps(event.to_cloudevents_dict())
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers={
                        "Authorization": f"Basic {self.auth_header}",
                        "Content-Type": "application/json"
                    }
                )

                if response.status_code == 200:
                    logger.info(f"Published event: {event.event_type} to {topic}")
                    return True
                else:
                    logger.error(f"Failed to publish: {response.status_code} - {response.text}")
                    return False

        except Exception as e:
            logger.error(f"Error publishing to Upstash Kafka: {e}")
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
        return await self.publish("task-events", event)


# Global publisher instance
_upstash_publisher: Optional[UpstashKafkaPublisher] = None


def get_upstash_publisher() -> UpstashKafkaPublisher:
    """Get or create the Upstash Kafka publisher."""
    global _upstash_publisher
    if _upstash_publisher is None:
        _upstash_publisher = UpstashKafkaPublisher()
    return _upstash_publisher


async def publish_task_event_upstash(
    event_type: TaskEventType,
    task_id: str,
    user_id: str = "anonymous",
    payload: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None
) -> bool:
    """
    Publish a task event to Upstash Kafka.
    Falls back to local logging if Upstash is not configured.
    """
    publisher = get_upstash_publisher()
    return await publisher.publish_task_event(
        event_type=event_type,
        task_id=task_id,
        user_id=user_id,
        payload=payload,
        correlation_id=correlation_id
    )
