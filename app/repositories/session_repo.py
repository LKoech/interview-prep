import json
from typing import Optional

from redis.asyncio import Redis

from app.models.session import InterviewSession
from app.repositories.base import BaseRepository


class SessionRepository(BaseRepository):
    """Redis-backed repository for interview sessions."""

    PREFIX = "session"
    DEFAULT_TTL = 86400  # 24 hours

    def __init__(self, redis: Redis):
        self._redis = redis

    def _key(self, session_id: str) -> str:
        return f"{self.PREFIX}:{session_id}"

    async def save(self, key: str, data: dict, ttl: Optional[int] = None) -> None:
        ttl = ttl or self.DEFAULT_TTL
        await self._redis.set(self._key(key), json.dumps(data, default=str), ex=ttl)

    async def get(self, key: str) -> Optional[dict]:
        raw = await self._redis.get(self._key(key))
        if raw is None:
            return None
        return json.loads(raw)

    async def delete(self, key: str) -> bool:
        result = await self._redis.delete(self._key(key))
        return result > 0

    async def list_keys(self, pattern: str = "*") -> list[str]:
        keys = []
        async for key in self._redis.scan_iter(f"{self.PREFIX}:{pattern}"):
            session_id = key.decode().removeprefix(f"{self.PREFIX}:")
            keys.append(session_id)
        return keys

    async def save_session(self, session: InterviewSession) -> InterviewSession:
        await self.save(session.id, session.model_dump())
        return session

    async def get_session(self, session_id: str) -> Optional[InterviewSession]:
        data = await self.get(session_id)
        if data is None:
            return None
        return InterviewSession(**data)

    async def list_sessions(self) -> list[InterviewSession]:
        keys = await self.list_keys()
        sessions = []
        for key in keys:
            session = await self.get_session(key)
            if session:
                sessions.append(session)
        return sessions
