import dataclasses
import logging

import requests

from exchange_api_clients.datastructs import ExchangeRate


class CoinGekoApiClient:
    EXCHANGE_COURSE_URL = 'https://api.coingecko.com/api/v3/simple/price?vs_currencies={}&ids={}'

    TOKEN_ABBREVIATURE_TO_COINGEKO_NAME = {
        'usdt': 'tether',
        'btc': 'bitcoin',
        'eth': 'ethereum',
    }

    def get_course(self, from_coin, to_coin):
        if from_coin in self.TOKEN_ABBREVIATURE_TO_COINGEKO_NAME.keys():
            from_coin = self.TOKEN_ABBREVIATURE_TO_COINGEKO_NAME[from_coin]
        elif to_coin in self.TOKEN_ABBREVIATURE_TO_COINGEKO_NAME.keys():
            to_coin = self.TOKEN_ABBREVIATURE_TO_COINGEKO_NAME[to_coin]
        resp = requests.get(self.EXCHANGE_COURSE_URL.format(to_coin, from_coin))
        if not resp.ok:
            logging.warning(f'ошибка ответа coingeko {resp.status_code}, {resp.text}')
            return None
        return dataclasses.asdict(
            ExchangeRate(
                from_coin_rate=1,
                from_coin=from_coin,
                to_coin_rate=resp.json()[from_coin][to_coin],
                to_coin=to_coin,
            ),
        )
