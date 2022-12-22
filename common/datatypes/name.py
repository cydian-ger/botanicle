from collections import UserString


class Name(UserString):
    def __init__(self, string: str):
        super().__init__(string)
