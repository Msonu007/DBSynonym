import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # SQL Server connection string (ODBC Driver 17 or 18)
    DATABASE_URL: str = (
        "sqlite+aiosqlite:///./synonyms.db"
    )

    # Cache backend: "inmemory" or "redis"
    CACHE_BACKEND: str = os.getenv("CACHE_BACKEND") if os.getenv("CACHE_BACKEND") else "inmemory"

    # Redis connection URL (if CACHE_BACKEND == "redis")
    REDIS_URL: str = "redis://localhost:6379/0"

    # Time‑to‑Live for cached synonym table (seconds)
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS")) if os.getenv("CACHE_TTL_SECONDS") else 600

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()