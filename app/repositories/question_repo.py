import json
from typing import Optional

from redis.asyncio import Redis

from app.models.question import Question
from app.repositories.base import BaseRepository


class QuestionRepository(BaseRepository):
    """Redis-backed repository for interview questions."""

    PREFIX = "question"
    SESSION_INDEX_PREFIX = "session_questions"
    DEFAULT_TTL = 86400

    def __init__(self, redis: Redis):
        self._redis = redis

    def _key(self, question_id: str) -> str:
        return f"{self.PREFIX}:{question_id}"

    def _session_index_key(self, session_id: str) -> str:
        return f"{self.SESSION_INDEX_PREFIX}:{session_id}"

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
            keys.append(key.decode().removeprefix(f"{self.PREFIX}:"))
        return keys

    async def save_question(self, question: Question) -> Question:
        await self.save(question.id, question.model_dump())
        # Add to session index (Redis Set)
        await self._redis.sadd(  # type: ignore[misc]
            self._session_index_key(question.session_id), question.id
        )
        return question

    async def get_question(self, question_id: str) -> Optional[Question]:
        data = await self.get(question_id)
        if data is None:
            return None
        return Question(**data)

    async def get_by_session(self, session_id: str) -> list[Question]:
        question_ids = await self._redis.smembers(  # type: ignore[misc]
            self._session_index_key(session_id)
        )
        questions = []
        for qid in question_ids:
            question = await self.get_question(qid.decode())
            if question:
                questions.append(question)
        return questions
