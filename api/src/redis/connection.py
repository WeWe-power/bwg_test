import redis.asyncio as redis

from redis.asyncio import Redis
from redis.exceptions import ConnectionError


from src.settings import settings


class RedisConnectionPool:

    pool = None
    instance = None

    def __new__(cls):
        if not hasattr(cls, 'instance') or not getattr(cls, 'instance'):
            cls.instance = super(RedisConnectionPool, cls).__new__(cls)
            cls.pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
            )
        return cls.instance

    @classmethod
    def get_conn(cls):
        return Redis(connection_pool=cls.pool)


async def get_redis_client() -> Redis | None:
    """
    Возвращает клиент для работы с Redis
    Если redis недоступен, вернется None
    """
    try:
        redis_client = RedisConnectionPool.get_conn()
        await redis_client.ping()
        return redis_client
    except ConnectionError:
        return None
