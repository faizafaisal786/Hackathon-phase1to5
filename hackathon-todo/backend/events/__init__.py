"""
Event publishing module - supports both Dapr and Upstash Kafka (FREE).
Automatically detects available backend and uses the appropriate publisher.
"""

import os
import logging
from typing import Optional, Dict, Any

from .models import TaskEventType, TaskEvent

logger = logging.getLogger(__name__)

# Detect which publisher to use
USE_UPSTASH = bool(os.getenv("UPSTASH_KAFKA_URL", ""))
USE_DAPR = bool(os.getenv("DAPR_HTTP_PORT", ""))


async def publish_task_event(
    event_type: TaskEventType,
    task_id: str,
    user_id: str = "anonymous",
    payload: Optional[Dict[str, Any]] = None,
    correlation_id: Optional[str] = None
) -> bool:
    """
    Smart event publisher - automatically selects backend.

    Priority:
    1. Upstash Kafka (FREE, serverless-friendly)
    2. Dapr Sidecar (Kubernetes deployments)
    3. Local logging (development/fallback)
    """

    if USE_UPSTASH:
        from .upstash_publisher import publish_task_event_upstash
        return await publish_task_event_upstash(
            event_type=event_type,
            task_id=task_id,
            user_id=user_id,
            payload=payload,
            correlation_id=correlation_id
        )

    if USE_DAPR:
        from .publisher import publish_task_event as publish_dapr
        return await publish_dapr(
            event_type=event_type,
            task_id=task_id,
            user_id=user_id,
            payload=payload,
            correlation_id=correlation_id
        )

    # Fallback to local logging
    logger.info(f"[LOCAL EVENT] {event_type.value}: task={task_id}, payload={payload}")
    return True


# Re-export for backwards compatibility
from .publisher import EventPublisher

__all__ = [
    "TaskEventType",
    "TaskEvent",
    "publish_task_event",
    "EventPublisher"
]
