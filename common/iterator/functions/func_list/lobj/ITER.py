from common.iterator.objects.LIterator import LIterator


# The production type
class ITER:
    # Stack size (amount of unclosed '[' preceding the cursor)
    @classmethod
    def stack(cls) -> int:
        return len(LIterator.stack)
