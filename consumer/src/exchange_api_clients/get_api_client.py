from exchange_api_clients.BinanceApiClient import BinanceApiClient
from exchange_api_clients.CoinGekoApiClient import CoinGekoApiClient


def get_api_client(exchange: str = 'binance'):
    if exchange == 'binance':
        return BinanceApiClient()
    elif exchange == 'coingeko':
        return CoinGekoApiClient()
    else:
        return None
