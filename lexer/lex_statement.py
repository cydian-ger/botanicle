from lexer.LT import LT
from typing import List, Tuple, Any

from lexer.lex_args import lex_args
from lexer.lex_error import LexError
from lexer.lex_expr import lex_expr
from lexer.lex_linebreak import lex_linebreak
from lexer.static import KEYWORDS, LINE_BREAK, ARG_OPEN, EXPR


def lex_statement(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    index = 0
    expr = ""

    while index < len(string):
        c = string[index]

        if c == " " or c == LINE_BREAK:
            if expr in KEYWORDS:
                token_list.append((LT.KEYWORD, expr))

            elif len(expr) > 0:
                # If the first char is a digit it will be a value
                if expr[0].isdigit():
                    token_list.append((LT.VALUE, expr))

                # If the first char is not a digit
                else:
                    token_list.append((LT.NAME, expr))

            if c == LINE_BREAK:
                index += lex_linebreak(string[index:], token_list)
                break

            expr = ""

        elif c == ARG_OPEN:
            # This means e.g. A(...) aka a symbol or many symbols in front of A arg group
            if len(expr) > 0:
                raise LexError(f"Arg open '{ARG_OPEN}' is not allowed to be preceded by anything but a space,"
                               " expr = '{expr}'", string[index:], SyntaxError)

            index += lex_args(string[index:], token_list)

        elif c == EXPR:
            index += lex_expr(string[index:], token_list)

        else:
            expr += c

        index += 1
    return index
