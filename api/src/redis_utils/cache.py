from redis_utils.structures import HashMap
from utils.time_utils import timestamp_now


# cache ttl in seconds
CACHE_TTL = 10


async def get_exchange_rate_from_cache(
    from_coin,
    to_coin,
    exchange: str = 'coingeko',
):
    exchange_data = HashMap(exchange)
    exchange_rate = await exchange_data.get(f'{from_coin}_{to_coin}_rate', raise_if_not_found=False)
    exchange_rate_update_ts = await exchange_data.get(f'{from_coin}_{to_coin}_update_ts', raise_if_not_found=False)
    if exchange_rate and timestamp_now() - exchange_rate_update_ts < CACHE_TTL:
        return exchange_rate
    return None
