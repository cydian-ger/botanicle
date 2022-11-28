from random import random


def seed(value1: float, value2: float, rounding: int = 0) -> float:
    _min = min(value1, value2)
    _max = max(value1, value2)
    return round(random() * (_max - _min) + _min, rounding)
