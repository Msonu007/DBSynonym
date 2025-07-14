import asyncio, time
from typing import Any, Optional
from .cache_base import CacheBackend

class InMemoryCache(CacheBackend):
    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            record = self._store.get(key)
            if not record:
                return None
            value, expires = record
            if expires < time.time():
                # Expired – remove lazily
                self._store.pop(key, None)
                return None
            return value

    async def set(self, key: str, value: Any, ttl: int) -> None:
        async with self._lock:
            self._store[key] = (value, time.time() + ttl)