import os

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_PORT: str = os.environ['RABBITMQ_PORT']
    RABBITMQ_HOST: str = os.environ['RABBITMQ_HOST']
    RABBITMQ_PASSWORD: str = os.environ['RABBITMQ_PASSWORD']
    RABBITMQ_USER: str = os.environ['RABBITMQ_USER']
    PARSE_EXCHANGE_COURSE_INTERVAL: int = int(os.environ.get('PARSE_EXCHANGE_COURSE_INTERVAL', 4))


settings = Settings()
