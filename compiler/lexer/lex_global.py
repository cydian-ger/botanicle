import sys
from typing import Tuple

from colorama import Back, Style

from common.LError import LError

Lexer = sys.modules[__name__]

Lexer.string = None


def init_lex(string: str):
    if Lexer.string is None:
        Lexer.string = string
    else:
        raise RuntimeError("Variable already defined")


def char(str_left: str):
    # str_left is the amount of string that is left
    return len(Lexer.string) - len(str_left)


def lraise(error: BaseException, err_pos: Tuple[int, int]):
    print(repr(error))
    print(f"{Lexer.string[:err_pos[0]]}"
          f"{Back.RED}{Lexer.string[err_pos[0]:err_pos[1]]}{Style.RESET_ALL}"
          f"{Lexer.string[err_pos[1]:]}")
    exit(0)
