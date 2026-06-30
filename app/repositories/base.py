"""Abstract base repository — defines the interface all repos must follow."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseRepository(ABC):
    """Repository pattern: abstracts data storage behind a consistent interface.

    Any backing store (Redis, PostgreSQL, in-memory) can implement this
    without changing the service layer.
    """

    @abstractmethod
    async def save(self, key: str, data: dict, ttl: Optional[int] = None) -> None:
        ...

    @abstractmethod
    async def get(self, key: str) -> Optional[dict]:
        ...

    @abstractmethod
    async def delete(self, key: str) -> bool:
        ...

    @abstractmethod
    async def list_keys(self, pattern: str) -> list[str]:
        ...
