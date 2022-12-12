from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.lex_args import lex_args
from compiler.lexer.static import VALID_RULE_LTOKENS, ARG_OPEN
from compiler.Lglobal import char


def lex_ltoken(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0  # Since we append string[0] already
    # arg = ""

    while len(string) > index:
        c = string[index]

        if c in VALID_RULE_LTOKENS and index == 0:
            # If this is the first character add it as the token
            token_list.append((LT.LTOKEN, None, char(string[index:])))
            token_list.append((LT.NAME, c, char(string[index:])))

        elif c == ARG_OPEN:
            index += lex_args(string[index:], token_list)
            # Add 1 because you are breaking
            index += 1
            # You can break here since either its closed or there is an error
            break

        else:
            token_list.append((LT.ARGS, None, char(string[index:])))
            token_list.append((LT.ARGS_END, None, char(string[index:])))
            # If the token is not A or A(...) then return after the first thing
            break

        index += 1

    token_list.append((LT.LTOKEN_END, None, char(string[index:])))
    return index
