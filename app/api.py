from fastapi import APIRouter, Depends
from .service import SynonymService
from .cache_inmemory import InMemoryCache
from .cache_redis import RedisCache
from .repository import get_session, SynonymRepository
from .config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from fastapi.responses import JSONResponse
import os
import sys
import time

router = APIRouter(prefix="/api", tags=["synonyms"])

# Dependency – Cache backend singleton per process
async def get_cache() -> InMemoryCache | RedisCache:
    if settings.CACHE_BACKEND == "redis":
        if not hasattr(get_cache, "_redis"):
            get_cache._redis = await RedisCache.create(settings.REDIS_URL)  # type: ignore[attr-defined]
        return get_cache._redis  # type: ignore[return-value]
    else:
        if not hasattr(get_cache, "_mem"):
            get_cache._mem = InMemoryCache()  # type: ignore[attr-defined]
        return get_cache._mem  # type: ignore[return-value]

# Dependency – Synonym service instance
async def get_service(
    cache: InMemoryCache | RedisCache = Depends(get_cache),
) -> SynonymService:
    return SynonymService(cache=cache, repo=SynonymRepository())

@router.get("/synonyms")
async def list_synonyms(
    service: SynonymService = Depends(get_service),
    session: AsyncSession = Depends(get_session),
):
    """Returns the full synonym table with metadata flag indicating cache hit."""
    return await service.get_all_synonyms(session=session)

@router.post("/update")
async def update_config(request: Request):
    data = await request.json()
    cache_backend = data.get("cache_backend", settings.CACHE_BACKEND)
    ttl = data.get("ttl", settings.CACHE_TTL_SECONDS)
    redis_url = data.get("redis_url", settings.REDIS_URL)

    # Update .env file
    with open(".env", "w") as f:
        f.write(f"CACHE_BACKEND={cache_backend}\n")
        f.write(f"CACHE_TTL_SECONDS={ttl}\n")
        f.write(f"REDIS_URL={redis_url}\n")
    os.environ["CACHE_BACKEND"] = cache_backend
    os.environ["CACHE_TTL_SECONDS"] = str(ttl)

    response = JSONResponse({"status": "updated, restarting..."})

    def restart():
        time.sleep(2)  # Wait for response to be sent
        os.execv(sys.executable, [sys.executable] + sys.argv)
    import threading
    threading.Thread(target=restart).start()

    return response