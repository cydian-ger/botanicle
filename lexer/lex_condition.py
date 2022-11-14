import re
from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.lex_args import lex_args
from lexer.static import RESULT_TOKEN, LINE_BREAK, ARG_OPEN


def lex_condition(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    token_list.append((LT.CONDITION, None))
    # TODO
    # Allow multiple arguments
    expr = ""
    index = 0

    while index < len(string):
        c = string[index]

        if c == RESULT_TOKEN or c == LINE_BREAK:
            break

        # Only allow list open if '(' appears and if the string is empty
        # e.g. don't allow 1*(a+b)
        elif c == ARG_OPEN and len(re.sub(' +', ' ', expr).lstrip(':').strip(' ')) == 0:
            index += lex_args(string[index:], token_list, (LT.ARGS, LT.CON_EXPR, LT.ARGS_END))
            index += 1
            break

        else:
            expr += c

        index += 1

    # Replace multiple spaces with a single one
    expr = re.sub(' +', ' ', expr)
    expr = expr.lstrip(':').strip(' ')  # Strip all spaces at the end and all : that precede the message

    if expr:
        token_list.append((LT.CON_EXPR, expr))

    token_list.append((LT.CONDITION_END, None))
    return index
