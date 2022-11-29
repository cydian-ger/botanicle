from compiler.lexer.LT import LT
from typing import List, Tuple, Any, Union

from compiler.lexer.lex_args import lex_args
from compiler.lexer.lex_error import LexError
from compiler.lexer.lex_expr import lex_expr
from compiler.lexer.lex_linebreak import lex_linebreak
from compiler.lexer.static import KEYWORDS, LINE_BREAK, ARG_OPEN, EXPR, PATH_CHARS
from compiler.Lglobal import char


def lex_statement(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0
    expr = ""

    while index < len(string):
        c = string[index]

        if c == " " or c == LINE_BREAK:
            if expr in KEYWORDS:
                token_list.append((LT.KEYWORD, expr, char(string[index:])))

            elif len(expr) > 0:
                # If the first char is a digit it will be a value
                if expr[0].isdigit():
                    token_list.append((LT.VALUE, expr, char(string[index:])))

                # If the expression contains path characters like "." and "/"
                elif len([character for character in PATH_CHARS if expr.__contains__(character)]) > 0:
                    token_list.append((LT.PATH, expr, char(string[index:])))
                # If the first char is not a digit
                else:
                    token_list.append((LT.NAME, expr, char(string[index:])))

            if c == LINE_BREAK:
                index += lex_linebreak(string[index:], token_list)
                break

            expr = ""

        elif c == ARG_OPEN:
            # This means e.g. A(...) aka a symbol or many symbols in front of A arg group
            if len(expr) > 0:
                raise LexError(f"Arg open '{ARG_OPEN}' is not allowed to be preceded by anything but a space,"
                               , string[index - 1:], SyntaxError)

            index += lex_args(string[index:], token_list)

        elif c == EXPR:
            index += lex_expr(string[index:], token_list)

        else:
            if not c.isalpha() and not c.isdigit() and c not in PATH_CHARS:
                raise LexError(f"Statement Keyword must be made up of only alphabetical characters and not '{c}'",
                               string[index:], SyntaxError)
            expr += c

        index += 1
    return index
