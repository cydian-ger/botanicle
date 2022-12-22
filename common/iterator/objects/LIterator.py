from common.iterator.objects import Turtle


class LIterator:
    stack: list[Turtle] = list()
    stack_size: int = lambda: len(LIterator.stack)
    index: int  # Counts in line, resets at carriage returns
    counter: int  # Counts 1 for every evaluated token

    @classmethod
    def flush(cls):
        cls.stack.clear()
        cls.index = 0
        cls.counter = 0
