from lexer.LT import LT
from typing import List, Tuple, Any
from lexer.lex_expr import lex_expr
from lexer.lex_function import lex_function
from lexer.static import ARG_CLOSE, ARG_DELIMITER, LINE_BREAK, EXPR, FUNCTION_TOKEN


def lex_args(string: str, token_list: List[Tuple[LT, Any]],
             arg_tokens: Tuple[LT, LT, LT] = (LT.ARGS, LT.ARG, LT.ARGS_END)) -> int:
    # arg_tokens: the tokens that start / end the args and the arg names.

    token_list.append((arg_tokens[0], None))
    # Start at 1 to forgo the open token, because you can only jump to this function if index[0] == ARG TOKEN
    index = 1
    arg = ""

    while index < len(string):
        c = string[index]

        if c == LINE_BREAK:
            # Linebreak before the arg end
            print(string, "\n", index, string[index:])
            raise SyntaxError

        elif c == ARG_CLOSE or c == ARG_DELIMITER:
            arg = arg.strip(" ")
            if arg != "":
                # Put the argument
                token_list.append((arg_tokens[1], arg))
                arg = ""

            if c == ARG_CLOSE:
                # Put the end argument name
                token_list.append((arg_tokens[2], None))
                break

        elif c == EXPR:
            index += lex_expr(string[index:], token_list)

        elif c == FUNCTION_TOKEN:
            index += lex_function(string[index:], token_list)
            continue
            # Continue to not count next sign
            # continue

        else:
            arg += c

        index += 1

    return index
