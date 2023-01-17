from typing import List, Any
from common.datatypes.LResult import LResult


class Line:
    history: List[List[Any]]
    predecessor: List[Any]
    successor: List[Any]

    @classmethod
    def new(cls, predecessor: List[LResult]):
        # Load the start line as the predecessor line
        cls.history = list()
        # Add the str of the name and the variables
        cls.predecessor = [[lres.name.data] + lres.load(dict()) for lres in predecessor]
        cls.successor = list()

    # https://en.wikipedia.org/wiki/Carriage_return#:~:text=A%20carriage%20return%2C%20sometimes%20known,of%20a%20line%20of%20text.
    @classmethod
    def carriage_return(cls):
        cls.history.append(cls.predecessor)
        cls.predecessor = cls.successor
        cls.successor = list()

    @classmethod
    def stash(cls):
        cls.history.append(cls.predecessor)
        cls.history.append(cls.successor)

    @classmethod
    def print(cls):
        out_str = ""
        for tkn in cls.successor:
            out_str += tkn[0]
            if len(tkn) > 1:
                out_str += "(" + ",".join(map(str, tkn[1:])) + ")"
        return out_str
