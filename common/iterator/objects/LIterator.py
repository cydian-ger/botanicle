from common.iterator.objects import Turtle


class LIterator:
    stack: list[Turtle] = list()
    index: int

    def __init__(self):
        self.stack = list()
        self.index = 0

    def flush(self):
        self.stack.clear()
        self.index = 0
