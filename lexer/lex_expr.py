from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.lex_error import LexError
from lexer.static import EXPR, LINE_BREAK


def lex_expr(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    index = 1
    expr = ""

    while index < len(string):
        c = string[index]

        if c == EXPR:
            token_list.append((LT.CON_EXPR, expr))
            break

        elif c == LINE_BREAK:
            raise LexError("Line break occured before closing of expression", string[index:], SyntaxError)

        expr += c
        index += 1

    return index
