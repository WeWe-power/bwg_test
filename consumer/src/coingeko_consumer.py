import json
import time

import pika

import logging

from exchange_api_clients.get_api_client import get_api_client
from rabbitmq.connection import get_rabbitmq_connection
from rabbitmq.message import ParseCryptoCoinExchangeRateMessage
from redis_utils.structures import HashMap
from utils.time_utils import timestamp_now

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dev')

RABBITMQ_QUEUE = 'coingeko_parser'
RABBITMQ_CONNECTION_ATTEMPTS = 6
RABBITMQ_CONNECTION_ATTEMPTS_INTERVAL = 10


def parse_exchange_rate(ch, method, properties, body):
    logger.info(f" [x] Received {body}")
    message = ParseCryptoCoinExchangeRateMessage.from_dict(json.loads(body))

    redis_hashmap = HashMap('coingeko')
    coingeko_api = get_api_client('coingeko')
    last_update_ts = redis_hashmap.get(
        f'{message.from_coin}_{message.to_coin}_update_ts',
        raise_if_not_found=False,
    )
    if last_update_ts and timestamp_now() - float(last_update_ts) < 2:
        logger.info(f'skipped update {message.from_coin}_{message.to_coin} course; recently updated')
        return None
    exchange_rate = coingeko_api.get_course(from_coin=message.from_coin, to_coin=message.to_coin)
    if exchange_rate:
        redis_hashmap.set(f'{message.from_coin}_{message.to_coin}_rate', exchange_rate['to_coin_rate'])
        redis_hashmap.set(f'{message.from_coin}_{message.to_coin}_update_ts', timestamp_now())
        logger.info(f'updated {message.from_coin}_{message.to_coin} course')

def main():
    connection = None
    for i in range(RABBITMQ_CONNECTION_ATTEMPTS):
        try:
            connection = get_rabbitmq_connection()
            channel = connection.channel()
        except pika.exceptions.AMQPConnectionError:
            logger.info(f'cannt connect to rabitmq, retrying in {RABBITMQ_CONNECTION_ATTEMPTS_INTERVAL} seconds')
            time.sleep(RABBITMQ_CONNECTION_ATTEMPTS_INTERVAL)
    if not connection:
        raise pika.exceptions.AMQPConnectionError()

    logger.info('connected to rabbitmq')
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        auto_ack=True,
        on_message_callback=parse_exchange_rate,
    )
    channel.start_consuming()


if __name__ == '__main__':
    main()
