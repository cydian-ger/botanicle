from typing import List, Any


class Line:
    history: List[List[Any]]
    predecessor: List[Any]
    successor: List[Any]

    @classmethod
    def new(cls, predecessor: List[Any]):
        # Load the start line as the predecessor line
        cls.history = list()
        cls.predecessor = predecessor
        cls.successor = list()

    # https://en.wikipedia.org/wiki/Carriage_return#:~:text=A%20carriage%20return%2C%20sometimes%20known,of%20a%20line%20of%20text.
    @classmethod
    def carriage_return(cls):
        cls.history.append(cls.predecessor)
        cls.predecessor = cls.successor
        cls.successor = list()
