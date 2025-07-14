from typing import Any, Dict
from .cache_base import CacheBackend
from .repository import SynonymRepository, get_session
from .config import settings

class SynonymService:
    _CACHE_KEY = "synonyms:all"

    def __init__(self, cache: CacheBackend, repo: SynonymRepository):
        self.cache = cache
        self.repo = repo
        self.ttl = settings.CACHE_TTL_SECONDS

    async def get_all_synonyms(self, session) -> Dict[str, Any]:
        cached = await self.cache.get(self._CACHE_KEY)
        if cached is not None:
            return {"from_cache": True, "items": cached}

        data = await self.repo.fetch_all(session=session)
        print(f"data is {data}")
        await self.cache.set(self._CACHE_KEY, data, self.ttl)
        return {"from_cache": False, "items": data}