from random import random


def seed(minimum: float, maximum: float, rounding: int = 0) -> float:
    """
seed returns a random value in the range [<minimum> : <maximum>].
<rounding> decides to which decimal point it is rounded (default = 0)
"""
    _min = min(minimum, maximum)
    _max = max(minimum, maximum)
    return round(random() * (_max - _min) + _min, rounding)
