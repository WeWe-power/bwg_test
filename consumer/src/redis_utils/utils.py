from redis_utils.connection import get_redis_client


def get_from_cache(key: str):
    conn = get_redis_client()
    return conn.get(key)
