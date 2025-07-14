import abc
from abc import abstractmethod
from typing import Any, Optional

class CacheBackend(abc.ABC):
    """Abstract cache backend with async interface."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int) -> None:
        pass
