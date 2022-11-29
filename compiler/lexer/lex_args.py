from compiler.lexer.LT import LT
from typing import List, Tuple, Any, Union

from compiler.lexer.lex_error import LexError
from compiler.lexer.lex_expr import lex_expr
from compiler.lexer.lex_function import lex_function
from compiler.lexer.lex_reference import lex_reference
from compiler.lexer.static import ARG_OPEN, ARG_CLOSE, ARG_DELIMITER, LINE_BREAK, EXPR, FUNCTION_TOKEN, REFERENCE_TOKEN, \
    EMPTY_ARGUMENT
from compiler.lexer.lex_global import char


def arg_strip(string: str) -> str:
    return string.strip(" ")


def lex_args(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]],
             arg_tokens: Tuple[LT, LT, LT] = (LT.ARGS, LT.ARG, LT.ARGS_END)) -> int:
    # arg_tokens: the tokens that start / end the args and the arg names.

    token_list.append((arg_tokens[0], None, char(string)))
    # Start at 1 to forgo the open token, because you can only jump to this function if index[0] == ARG TOKEN
    index = 1
    arg = ""

    while index < len(string):
        c = string[index]

        if c == LINE_BREAK:
            # Linebreak before the arg end
            raise LexError("Linebreak before the end of an arg", string[index:], SyntaxError)

        elif c == ARG_OPEN:
            index += lex_args(string[index:], token_list)
            # raise LexError(f"Can not open args '{ARG_OPEN}' while inside of args", string[index:], SyntaxError)

        elif c == ARG_CLOSE or c == ARG_DELIMITER:
            arg = arg.strip(" ")

            if arg != "":
                if arg == EMPTY_ARGUMENT:
                    token_list.append((arg_tokens[1], "", char(string[index:])))

                else:
                    # Put the argument
                    token_list.append((arg_tokens[1], arg, char(string[index:])))
                    arg = ""

            if c == ARG_CLOSE:
                # Put the end argument name
                token_list.append((arg_tokens[2], None, char(string[index + 1:])))
                break

        elif c == EXPR:
            index += lex_expr(string[index:], token_list, expr_type=LT.EXPR)

        elif c == FUNCTION_TOKEN:
            if arg_strip(arg) != "":
                raise LexError(f"Function token '{FUNCTION_TOKEN} has to be the first character of the argument."
                               , string[index:], SyntaxError)

            index += lex_function(string[index:], token_list)
            continue
            # Continue to not count next sign
            # continue

        elif c == REFERENCE_TOKEN:
            if arg_strip(arg) != "":
                raise LexError(f"Reference token '{REFERENCE_TOKEN} has to be the first character of the argument."
                               , string[index:], SyntaxError)

            index += lex_reference(string[index:], token_list)
            continue

        else:
            arg += c

        index += 1

    return index
