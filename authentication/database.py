from functools import lru_cache
from typing import Iterator

from alembic import command
from alembic.config import Config
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from sqlmodel import create_engine
from authentication.settings import Settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """
    Creates a postgres engine
    """
    settings = Settings()
    postgres_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"  # pylint: disable=line-too-long
    return create_engine(
        postgres_url,
        pool_size=100,
        max_overflow=30,
        pool_use_lifo=True,
        pool_pre_ping=True,
        pool_timeout=25,
        pool_recycle=1800,
        connect_args={
            "connect_timeout": 10,  # Timeout for establishing a connection
            "keepalives": 1,  # Enable TCP keepalive
            "keepalives_idle": 30,  # Idle time before sending keepalive probes
            "keepalives_interval": 10,  # Time between keepalive probes
            "keepalives_count": 5,  # Number of failed probes before closing the connection
        },
    )


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Iterator[SQLAlchemySession]:
    with SessionLocal() as session:
        yield session


def run_alembic_migrations() -> None:
    """
    Runs alembic migrations
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
