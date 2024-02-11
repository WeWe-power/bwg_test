import dataclasses
import json

import requests
from websocket import create_connection

from exchange_api_clients.datastructs import ExchangeRate
from exchange_api_clients.exceptions import BinanceApiError


class BinanceApiClient:
    instance = None
    ws = None

    BINANCE_WEBSOCKET_API_URL = 'wss://ws-api.binance.com:443/ws-api/v3'
    GET_USD_TO_RUB_EXCHANGE_RATE_URL = 'https://www.binance.com/bapi/asset/v1/public/asset-service/product/currency'

    def __new__(cls):
        if not hasattr(cls, 'instance') or not getattr(cls, 'instance'):
            cls.instance = super(BinanceApiClient, cls).__new__(cls)
            cls.ws = create_connection(cls.BINANCE_WEBSOCKET_API_URL)
        return cls.instance

    def __enter__(self):
        self.ws = create_connection(self.BINANCE_WEBSOCKET_API_URL)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Заканчиваем сессию в storm после использования контекстного менеджера"""
        self.ws.close()
        self.ws = None
        return False

    def get_course(self, from_coin, to_coin):
        if not self.ws:
            raise BinanceApiError('Соединено с binance ws api не открыто')
        print(from_coin, to_coin)
        self.ws.send(
            json.dumps(
                {
                  "id": "ddbfb65f-9ebf-42ec-8240-8f0f91de0867",
                  "method": "avgPrice",
                  "params": {
                    "symbol": f"{from_coin.upper()}{to_coin.upper()}",
                  },
                },
            ),
        )
        resp = json.loads(self.ws.recv())
        if resp['status'] == 400:
            return None
        return dataclasses.asdict(
            ExchangeRate(
                from_coin=from_coin,
                from_coin_rate=1,
                to_coin=to_coin,
                to_coin_rate=round(float(resp['result']['price']), 5)
            )
        )

    def get_usd_to_rub_exchange_rate(self):
        resp = requests.get('https://www.binance.com/bapi/asset/v1/public/asset-service/product/currency')
        if not resp.ok:
            raise BinanceApiError('Ошибка при получении курса обмена доллара к рублю')
        for data in resp.json()['data']:
            if data['pair'] == 'RUB_USD':
                return dataclasses.asdict(
                    ExchangeRate(
                        from_coin='usd',
                        from_coin_rate=1,
                        to_coin='rub',
                        to_coin_rate=round(float(data['rate']), 5)
                    )
                )
