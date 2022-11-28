import sys
from typing import Tuple, Union

from common.LError import LError

Lexer = sys.modules[__name__]

Lexer.string = None


def init_lex(string: str):
    if Lexer.string is None:
        Lexer.string = string
    else:
        raise RuntimeError("Variable already defined")


def get_char(str_left: str):
    # str_left is the amount of string that is left
    return Lexer.string - len(str_left)


def throw_error(error: LError, error_position:Tuple[int, int]):
    pass
