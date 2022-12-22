from collections import UserString
from typing import Union, Tuple

from compiler.Lglobal import lraise


class Token(UserString):
    def __init__(self, string: str, token_index: Union[int, Tuple[int, int]]):
        super().__init__(string)

        if len(self) != 1:
            lraise(SyntaxError(f"Token '{self}' has to have the length of 1 but has length {len(self)}"),
                   token_index)
