from collections import UserString


class Name(UserString):
    def __init__(self, string: str, token_index):
        super().__init__(string)
