import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_PORT: str = os.environ['RABBITMQ_PORT']
    RABBITMQ_HOST: str = os.environ['RABBITMQ_HOST']
    RABBITMQ_PASSWORD: str = os.environ['RABBITMQ_PASSWORD']
    RABBITMQ_USER: str = os.environ['RABBITMQ_USER']
    REDIS_HOST: str = os.environ['REDIS_HOST']
    REDIS_PORT: str = os.environ['REDIS_PORT']
    REDIS_DB: str = os.environ['REDIS_DB']


settings = Settings()
