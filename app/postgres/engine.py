from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import Config


engine = create_async_engine(Config.postgres_url, future=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
