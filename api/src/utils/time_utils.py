from datetime import datetime


def timestamp_now() -> float:
    """Возвращает текущий timestamp"""
    return datetime.now().timestamp()
