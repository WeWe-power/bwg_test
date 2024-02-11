import dataclasses
import json
import logging
import time

import pika

from rabbitmq.message import ParseCryptoCoinExchangeRateMessage
from rabbitmq.connection import get_rabbitmq_connection
from settings import settings

RABBITMQ_CONNECTION_ATTEMPTS = 6
RABBITMQ_CONNECTION_ATTEMPTS_INTERVAL = 10

BINANCE_COURSES_PARSER_QUEUE = 'binance_parser'
COINGEKO_COURSES_PARSER_QUEUE = 'coingeko_parser'
queues = [BINANCE_COURSES_PARSER_QUEUE, COINGEKO_COURSES_PARSER_QUEUE]

FROM_COINS = ['btc', 'usdt', 'eth']
TO_COINS = ['usd', 'rub']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dev')


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

    channel.queue_declare(queue=BINANCE_COURSES_PARSER_QUEUE)
    channel.queue_declare(queue=COINGEKO_COURSES_PARSER_QUEUE)

    try:
        while True:
            logger.info('sending messages')
            for from_coin in FROM_COINS:
                for to_coin in TO_COINS:
                    message = ParseCryptoCoinExchangeRateMessage(from_coin=from_coin, to_coin=to_coin)
                    for queue in queues:
                        channel.basic_publish(
                            exchange='',
                            routing_key=queue,
                            body=json.dumps(dataclasses.asdict(message)),
                        )
            time.sleep(settings.PARSE_EXCHANGE_COURSE_INTERVAL)
    except Exception as ex:
        logger.error(ex)
        raise ex
    finally:
        connection.close()

if __name__ == "__main__":
    main()
