from types import LambdaType


class Proxy:
    parent: object

    def __init__(self, parent: object):
        self.parent = parent

    def __getattribute__(self, item):
        # If there is a lambda, call it
        ret = super(Proxy, self).__getattribute__(item)
        if isinstance(ret, LambdaType):
            return ret()
        else:
            return ret
