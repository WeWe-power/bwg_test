from redis.exceptions import ResponseError

from redis_utils.connection import get_redis_client
from redis_utils.exceptions import KeyDoesNotExists


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
    async def get(self, key='', raise_if_not_found=True):
        await self.check_conn()
        try:
            return await self.conn.json().get(self.name, f'.{key}')
        except ResponseError:
            if raise_if_not_found:
                raise KeyDoesNotExists(f'Ключа {key} не существует')
