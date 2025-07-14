import json
from typing import Any, Optional
import redis
from redis import asyncio as async_redis
from .cache_base import CacheBackend

class RedisCache(CacheBackend):
    def __init__(self, redis_client):
        self._redis: async_redis.Redis = redis_client

    @classmethod
    async def create(cls, url: str) -> "RedisCache":
        redis_ = async_redis.from_url(url, decode_responses=False)
        # Ping to confirm connection
        await redis_.ping()
        return cls(redis_)

    async def get(self, key: str) -> Optional[Any]:
        raw = await self._redis.get(key)
        return json.loads(raw) if raw else None

    async def set(self, key: str, value: Any, ttl: int) -> None:
        await self._redis.set(key, json.dumps(value, default=str).encode(), ex=ttl)
