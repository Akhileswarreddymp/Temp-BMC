from functools import lru_cache
from typing import AsyncGenerator

from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from authentication.settings import Settings


@lru_cache(maxsize=1)
def get_engine():
    settings = Settings()
    postgres_url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    return create_async_engine(
        postgres_url,
        pool_size=100,
        max_overflow=30,
        pool_use_lifo=True,
        pool_pre_ping=True,
        pool_timeout=25,
        pool_recycle=1800,
    )

engine = get_engine()

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
            yield session



def run_alembic_migrations() -> None:
    """
    Runs alembic migrations
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
