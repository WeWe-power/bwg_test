from fastapi import FastAPI

from v1.courses import courses_router

app = FastAPI()
app.include_router(
    courses_router,
    prefix="/v1",
    tags=["courses"],
)
