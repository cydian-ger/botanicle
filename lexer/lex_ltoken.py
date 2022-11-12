from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.lex_args import lex_args
from lexer.lex_function import lex_function
from lexer.static import VALID_RULE_LTOKENS, ARG_OPEN, FUNCTION_TOKEN


def lex_ltoken(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    index = 0  # Since we append string[0] already
    arg = ""

    while len(string) > index:
        c = string[index]

        if c in VALID_RULE_LTOKENS:
            # If this is the first character add it as the token
            if index == 0:
                token_list.append((LT.LTOKEN, c))
            else:
                break

        elif c == ARG_OPEN:
            index += lex_args(string[index:], token_list)
            # Add 1 because you are breaking
            index += 1
            # You can break here since either its closed or there is an error
            break

        else:
            # If the token is not A or A(...) then return after the first thing
            break

        index += 1

    return index
