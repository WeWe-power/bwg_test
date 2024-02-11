from fastapi import APIRouter

courses_router = APIRouter()


@courses_router.get("/courses/", tags=["courses"])
async def courses(from_coin: str = 'btc', to_coin: str = 'usd'):
    return [{"username": "Rick"}, {"username": "Morty"}]