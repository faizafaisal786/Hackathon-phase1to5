"""
Upstash Kafka Client for Reminder Service - 100% FREE
"""

import os
import logging
import base64
import json
from typing import Optional, Dict, Any, List

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

logger = logging.getLogger(__name__)

# Upstash Kafka Configuration (FREE tier)
UPSTASH_KAFKA_URL = os.getenv("UPSTASH_KAFKA_URL", "")
UPSTASH_KAFKA_USERNAME = os.getenv("UPSTASH_KAFKA_USERNAME", "")
UPSTASH_KAFKA_PASSWORD = os.getenv("UPSTASH_KAFKA_PASSWORD", "")


class UpstashKafka:
    """
    Upstash Kafka client using REST API.
    Works perfectly with FREE tier - 10,000 messages/day.
    """

    def __init__(self):
        self.base_url = UPSTASH_KAFKA_URL.rstrip('/') if UPSTASH_KAFKA_URL else ""
        self.username = UPSTASH_KAFKA_USERNAME
        self.password = UPSTASH_KAFKA_PASSWORD
        self.enabled = bool(self.base_url and self.username and HTTPX_AVAILABLE)

        if self.enabled:
            credentials = f"{self.username}:{self.password}"
            self.auth_header = base64.b64encode(credentials.encode()).decode()
            logger.info("Upstash Kafka initialized (FREE tier)")
        else:
            logger.info("Upstash Kafka not configured - using local mode")

    async def produce(self, topic: str, message: Dict[str, Any]) -> bool:
        """Produce a message to a topic."""
        if not self.enabled:
            logger.info(f"[LOCAL] Would publish to {topic}: {message.get('event_type', 'event')}")
            return True

        try:
            url = f"{self.base_url}/produce/{topic}"
            payload = {"value": json.dumps(message)}

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
                    logger.info(f"Published to {topic}")
                    return True
                else:
                    logger.error(f"Failed to publish: {response.status_code}")
                    return False

        except Exception as e:
            logger.error(f"Upstash Kafka error: {e}")
            return False

    async def consume(self, topic: str, group: str, instance: str = "reminder-1") -> List[Dict]:
        """Consume messages from a topic."""
        if not self.enabled:
            return []

        try:
            url = f"{self.base_url}/consume/{group}/{instance}/{topic}"

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    url,
                    headers={"Authorization": f"Basic {self.auth_header}"}
                )

                if response.status_code == 200:
                    data = response.json()
                    messages = []
                    for item in data:
                        try:
                            value = json.loads(item.get("value", "{}"))
                            messages.append(value)
                        except json.JSONDecodeError:
                            pass
                    return messages
                return []

        except Exception as e:
            logger.error(f"Upstash Kafka consume error: {e}")
            return []


# Global instance
_kafka: Optional[UpstashKafka] = None


def get_kafka() -> UpstashKafka:
    """Get Upstash Kafka client."""
    global _kafka
    if _kafka is None:
        _kafka = UpstashKafka()
    return _kafka


async def publish_reminder_event(
    reminder_id: str,
    task_id: str,
    user_id: str,
    task_title: str,
    due_date: str,
    minutes_until_due: int,
    task_priority: int = 0
) -> bool:
    """Publish reminder event to Upstash Kafka (FREE)."""
    kafka = get_kafka()

    event = {
        "event_type": "reminder.triggered",
        "reminder_id": reminder_id,
        "task_id": task_id,
        "user_id": user_id,
        "task_title": task_title,
        "task_priority": task_priority,
        "due_date": due_date,
        "minutes_until_due": minutes_until_due,
        "channels": ["push", "email", "in_app"]
    }

    return await kafka.produce("reminder-events", event)
