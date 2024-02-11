from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from redis_utils.cache import get_exchange_rate_from_cache

courses_router = APIRouter()


class Course(BaseModel):
    direction: str = 'BTC-USD'
    value: str


class ExchangeRateInfo(BaseModel):
    exchanger: str = 'coingeko'
    course: Course


@courses_router.get("/courses/", tags=["courses"], response_model=ExchangeRateInfo)
async def courses(from_coin: str = 'btc', to_coin: str = 'usd'):
    """
    Получить данные о курсах криптовалют к рублю/доллару
    from_coin - криптовалюта, btc/eth/usdt
    to_coin - фиат, usd / rub
    """
    for exchange in ['coingeko', 'binance']:
        exchange_rate = await get_exchange_rate_from_cache(
            exchange=exchange,
            from_coin=from_coin,
            to_coin=to_coin,
        )
        if exchange_rate:
            return ExchangeRateInfo(
                exchanger=exchange,
                course=Course(direction=f'{from_coin}_{to_coin}', value=str(exchange_rate)),
            )
    raise HTTPException(status_code=400, detail="Нету данных по актуальному курсу")
