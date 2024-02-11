from dataclasses import dataclass


@dataclass
class ParseCryptoCoinCourseMessage:
    from_coin: str
    to_coin: str
