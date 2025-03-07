from functools import lru_cache
from typing import Iterator

from alembic import command
from alembic.config import Config
from sqlalchemy.future import Engine
from sqlmodel import Session, create_engine, sessionmaker
from authentication.settings import Settings

@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """
    Creates a postgres engine
    """
    postgres_url = f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/zn_tanklayouts"  # pylint: disable=line-too-long
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
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


def run_alembic_migrations() -> None:
    """
    Runs alembic migrations
    """
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")