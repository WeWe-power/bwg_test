from dataclasses import dataclass


@dataclass
class ParseCryptoCoinExchangeRateMessage:
    from_coin: str
    to_coin: str

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
