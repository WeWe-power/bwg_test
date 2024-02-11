from dataclasses import dataclass


@dataclass
class ParseCryptoCoinExchangeRateMessage:
    from_coin: str
    to_coin: str
