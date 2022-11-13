import re
from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.static import RESULT_TOKEN, LINE_BREAK


def lex_condition(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    token_list.append((LT.CONDITION, None))
    # TODO
    # Allow multiple arguments
    expr = ""
    for index, c in enumerate(string):
        if c == RESULT_TOKEN or c == LINE_BREAK:
            break
        else:
            expr += c

    length = len(expr)
    # Replace multiple spaces with a single one
    expr = re.sub(' +', ' ', expr)
    expr = expr.lstrip(':').strip(' ')  # Strip all spaces at the end and all : that precede the message

    if expr:
        token_list.append((LT.CON_EXPR, expr))

    token_list.append((LT.CONDITION_END, None))
    return length
