# type: ignore
import asyncio
import aioredis
from authentication.settings import Settings

class RedisClient:
    _pool = None
    _client = None
    _lock = asyncio.Lock()

    @classmethod
    async def _initialize(cls):
        """Initialize Redis connection pool and async client."""
        settings = Settings()
        if cls._pool is None:
            cls._pool = aioredis.ConnectionPool.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                decode_responses=True,
                max_connections=100,
            )

        cls._client = aioredis.Redis(connection_pool=cls._pool)

        try:
            await cls._client.ping()
        except Exception as exception:
            cls._client = None
            cls._pool = None
            raise RuntimeError(f"Redis connection failed: {exception}") from exception

    @classmethod
    async def get_client(cls):
        """Returns an async Redis client instance with connection pooling."""
        async with cls._lock:
            if cls._client is None:
                await cls._initialize()
        return cls._client

async def get_redis_client():
    """FastAPI dependency for async Redis client."""
    try:
        return await RedisClient.get_client()
    except RuntimeError as error:
        raise RuntimeError(f"Redis connection error: {error}") from error
