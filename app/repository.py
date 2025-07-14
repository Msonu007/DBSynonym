from typing import List
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .models import Synonym
from .config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

class SynonymRepository:
    """DAL for synonym CRUD – only batch read required."""

    async def fetch_all(self, session: AsyncSession) -> List[dict]:
        result = await session.execute(select(Synonym))
        l = result.all()
        return [row[0].model_dump() for row in l]
