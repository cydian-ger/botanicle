from common.iterator.objects import Turtle


class LIterator:
    stack: list[Turtle] = list()
    stack_size: int = lambda: len(LIterator.stack)
    index: int

    @classmethod
    def flush(cls):
        cls.stack.clear()
        cls.index = 0
