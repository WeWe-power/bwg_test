from redis import Redis
from redis.exceptions import ConnectionError


from settings import settings


def get_redis_client() -> Redis | None:
    """
    Возвращает клиент для работы с Redis
    Если redis недоступен, вернется None
    """
    try:
        redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        redis_client.ping()
        return redis_client
    except ConnectionError:
        return None
