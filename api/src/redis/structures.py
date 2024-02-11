from redis.exceptions import ResponseError

from src.redis.connection import get_redis_client
from src.redis.exceptions import KeyDoesNotExists


class RedisStruct:

    def __init__(self, name, conn=None):
        self.conn = conn
        self.name = name

    async def is_created(self):
        try:
            return bool(await self.conn.exists(self.name))
        except AttributeError:
            return False

    async def check_conn(self):
        if not self.conn:
            self.conn = await get_redis_client()

    async def flush(self):
        return await self.conn.delete(self.name)


class HashMap(RedisStruct):
    async def get(self, key=''):
        await self.check_conn()
        try:
            return await self.conn.json().get(self.name, f'.{key}')
        except ResponseError:
            raise KeyDoesNotExists(f'Ключа {key} не существует')
