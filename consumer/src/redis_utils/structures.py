from redis.exceptions import ResponseError

from redis_utils.connection import get_redis_client
from redis_utils.exceptions import KeyDoesNotExists


class RedisStruct:

    def __init__(self, name, conn=None):
        self.conn = conn
        self.name = name

    def is_created(self):
        try:
            return bool(self.conn.exists(self.name))
        except AttributeError:
            return False

    def check_conn(self):
        if not self.conn:
            self.conn = get_redis_client()

    def flush(self):
        return self.conn.delete(self.name)


class HashMap(RedisStruct):

    def create_in_redis(self):
        self.check_conn()
        if not self.is_created():
            self.conn.json().set(self.name, '.', {})

    def set(self, key, value):
        self.check_conn()
        try:
            self.conn.json().set(self.name, f'.{key}', value)
        except ResponseError:
            self.create_in_redis()
            self.conn.json().set(self.name, f'.{key}', value)
        return True

    def get(self, key='', raise_if_not_found: bool = True):
        self.check_conn()
        try:
            return self.conn.json().get(self.name, f'.{key}')
        except ResponseError:
            if raise_if_not_found:
                raise KeyDoesNotExists(f'Ключа {key} не существует')
