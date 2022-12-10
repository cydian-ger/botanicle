from typing import List, Any


class Line:
    history: List[List[Any]]
    predecessor: List[Any]
    successor: List[Any]

    def __init__(self, predecessor: List[Any]):
        # Load the start line as the predecessor line
        self.history = list()
        self.predecessor = predecessor
        self.successor = list()

    # https://en.wikipedia.org/wiki/Carriage_return#:~:text=A%20carriage%20return%2C%20sometimes%20known,of%20a%20line%20of%20text.
    def carriage_return(self):
        self.history.append(self.predecessor)
        self.predecessor = self.successor
        self.successor = list()
