import redis
from threading import Lock
from authentication.settings import Settings


class RedisClient:
    _pool = None
    _client = None
    _lock = Lock()

    @classmethod
    def _initialize(cls):
        """Initialize Redis connection pool and client."""
        settings = Settings()
        if cls._pool is None:
            cls._pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                max_connections=100,
                decode_responses=True
            )

        cls._client = redis.Redis(connection_pool=cls._pool)

        try:
            cls._client.ping()
        except Exception as exception:
            cls._client = None
            cls._pool = None
            raise RuntimeError(f"Redis connection failed {exception}")

    @classmethod
    def get_client(cls):
        """Returns a Redis client instance."""
        if cls._client is None:
            with cls._lock:
                if cls._client is None:
                    cls._initialize()
        return cls._client


def get_redis_client():
    """FastAPI dependency for Redis client."""
    try:
        return RedisClient.get_client()
    except RuntimeError as e:
        raise RuntimeError(f"Redis connection error: {e}")
