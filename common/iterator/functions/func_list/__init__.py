__all__ = ['seed', 'maximum',  # functions
           "Turtle", "LIterator",
           "lobjects", "lfunctions"]  # objects

# Functions
from .lfunc import seed, maximum

# Objects
from common.iterator.objects.turtle import Turtle
from common.iterator.objects.LIterator import LIterator


def lfunctions():
    return [func for func in __all__ if not (func.startswith("_") or func[0].isupper())]


def lobjects():
    return [obj for obj in __all__ if not (obj.startswith("_") or obj[0].islower())]
