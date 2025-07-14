import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.api import router as api_router
from app.models import Synonym
from app.repository import engine
from sqlmodel import SQLModel
import random

async def insert_data():
    async with AsyncSession(engine) as session:
        syns = ['joyfull','cheerfull']
        syn = Synonym(
            word_id=random.randint(0,1000000),
            word="happy",
            synonyms_json = " ".join(syns)
        )
        session.add(syn)
        await session.commit()

@asynccontextmanager
async def on_startup(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        await insert_data()
    yield
    await engine.dispose()

app = FastAPI(title="DataEngineSynonymSystem",
              lifespan=on_startup)
app.include_router(api_router)

