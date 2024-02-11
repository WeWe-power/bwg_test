from sqlmodel import SQLModel, Field


class CryptoExchange(SQLModel, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str


class CryptoCoin(SQLModel, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    name: str
    abbreviation: str
