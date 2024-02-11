from dataclasses import dataclass


@dataclass
class ExchangeRate:
    from_coin: str
    from_coin_rate: float | int
    to_coin: str
    to_coin_rate: float | int
