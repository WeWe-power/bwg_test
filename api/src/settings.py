import os

from pydantic.v1 import BaseSettings


def get_db_url(db_user, db_pass, db_host, db_port, db_name):
    return f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'


class Settings(BaseSettings):
    DB_CONNECTION_URL: str = get_db_url(
        db_user=os.environ['DB_USER'],
        db_pass=os.environ['DB_PASSWORD'],
        db_host=os.environ['DB_HOST'],
        db_port=os.environ['DB_PORT'],
        db_name=os.environ['DB_NAME'],
    )
    REDIS_HOST: str = os.environ['REDIS_HOST']
    REDIS_PORT: str = os.environ['REDIS_PORT']
    REDIS_DB: str = os.environ['REDIS_DB']


settings = Settings()
