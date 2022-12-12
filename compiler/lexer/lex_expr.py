from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.static import EXPR, LINE_BREAK
from compiler.Lglobal import char, lraise


def lex_expr(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]], expr_type=LT.CON_EXPR) -> int:
    index = 1
    expr = ""

    while index < len(string):
        c = string[index]

        if c == EXPR:
            token_list.append((expr_type, expr, char(string[index:])))
            break

        elif c == LINE_BREAK:
            lraise(SyntaxError("Line break occurred before closing of expression_functions"), char(string[index:]))

        expr += c
        index += 1

    return index
