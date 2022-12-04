from compiler.Lglobal.objects.LIterator import LIterator


# The iterator type
class ITER:
    # Count method: returns the iteration number this iterator is currently on.
    @classmethod
    def index(cls) -> int:
        return LIterator.index

    # Stack size (amount of unclosed '[' preceding the cursor)
    @classmethod
    def stack(cls) -> int:
        return len(LIterator.stack)
