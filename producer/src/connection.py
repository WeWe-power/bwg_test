import pika

from settings import settings


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        settings.RABBITMQ_HOST,
        settings.RABBITMQ_PORT,
        '/',
        credentials,
    )
    return pika.BlockingConnection(parameters)
