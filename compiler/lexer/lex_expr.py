from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.lex_error import LexError
from compiler.lexer.static import EXPR, LINE_BREAK
from compiler.lexer.lex_global import char


def lex_expr(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]], expr_type=LT.CON_EXPR) -> int:
    index = 1
    expr = ""

    while index < len(string):
        c = string[index]

        if c == EXPR:
            token_list.append((expr_type, expr, char(string[index:])))
            break

        elif c == LINE_BREAK:
            raise LexError("Line break occured before closing of expression", string[index:], SyntaxError)

        expr += c
        index += 1

    return index
