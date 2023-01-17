import re
from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.lex_args import lex_args
from compiler.lexer.static import RESULT_TOKEN, LINE_BREAK, ARG_OPEN, CONDITION_TOKEN, SPACE, EXPR
from compiler.Lglobal import char, lraise


def _strip_expr(expr: str) -> str:
    return re.sub(' +', ' ', expr).lstrip(':').strip(' ')


def lex_condition(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    token_list.append((LT.CONDITION, None, char(string)))
    expr = ""
    index = 0

    while index < len(string):
        c = string[index]

        if c == RESULT_TOKEN or c == LINE_BREAK:
            break

        elif c == CONDITION_TOKEN and index != 0:
            lraise(SyntaxError("Condition token can not appear more than once in a rule"), char(string[index:]))

        # Only allow list open if '(' appears and if the string is empty
        # e.g. don't allow 1*(a+b)
        elif c == ARG_OPEN and len(_strip_expr(expr)) == 0:
            index += lex_args(string[index:], token_list, (LT.ARGS, LT.CON_EXPR, LT.ARGS_END))
            index += 1
            break

        else:
            expr += c

        index += 1

    if _strip_expr(expr):
        # Calculate the right pad
        right_pad = 0
        for r in reversed(expr):
            if r in {SPACE}:
                right_pad += 1
            else:
                break

        expr = _strip_expr(expr)  # Strip all spaces at the end and all : that precede the message

        token_index = (
            char(string[index:]) - right_pad - len(expr) + 1,  # Start of token
            char(string[index:]) - right_pad + 1  # End of token
        )

        if expr[-1] != EXPR and expr[0] != EXPR:
            lraise(SyntaxError(f"Expression needs to be wrapped using <{EXPR}>."), token_index)

        token_list.append((LT.CON_EXPR, expr, token_index))

    token_list.append((LT.CONDITION_END, None, char(string[index:])))
    return index
