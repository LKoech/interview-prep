"""Observer pattern via Redis pub/sub.

Components publish events (e.g. "session_created") and handlers
react without the publisher knowing who's listening. This decouples
the API layer from side-effects like question generation.
"""

import asyncio
import json
import logging
from collections import defaultdict
from typing import Any, Callable, Coroutine

from redis.asyncio import Redis

logger = logging.getLogger(__name__)

Handler = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class EventBus:

    CHANNEL = "interview_events"

    def __init__(self, redis: Redis):
        self._redis = redis
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self._pubsub = None
        self._listener_task = None

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event_type: str, data: dict[str, Any]) -> None:
        message = json.dumps({"event": event_type, "data": data})
        await self._redis.publish(self.CHANNEL, message)

    async def _listen(self) -> None:
        self._pubsub = self._redis.pubsub()
        await self._pubsub.subscribe(self.CHANNEL)
        async for message in self._pubsub.listen():
            if message["type"] != "message":
                continue
            try:
                payload = json.loads(message["data"])
                event_type = payload["event"]
                data = payload["data"]
                for handler in self._handlers.get(event_type, []):
                    await handler(data)
            except Exception:
                logger.exception("Error handling event")

    async def start(self) -> None:
        self._listener_task = asyncio.create_task(self._listen())

    async def stop(self) -> None:
        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
        if self._pubsub:
            await self._pubsub.unsubscribe(self.CHANNEL)
            await self._pubsub.close()
