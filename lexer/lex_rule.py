from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.lex_args import lex_args
from lexer.lex_assignment import lex_assignment
from lexer.lex_function import lex_function
from lexer.lex_linebreak import lex_linebreak
from lexer.lex_ltoken import lex_ltoken
from lexer.lex_condition import lex_condition
from lexer.static import VALID_RULE_LTOKENS, CONTEXT_TOKENS, CONDITION_TOKEN, RESULT_TOKEN, LINE_BREAK, \
    ASSIGNMENT_TOKEN, FUNCTION_TOKEN, ARG_OPEN


def lex_rule(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    index = 0

    while index < len(string):
        c = string[index]

        if c in VALID_RULE_LTOKENS:
            index += lex_ltoken(string[index:], token_list)

        elif c == ASSIGNMENT_TOKEN:
            if index > 0:
                raise SyntaxError
            else:
                index += lex_assignment(string[index:], token_list)

        elif c == FUNCTION_TOKEN:
            index += lex_function(string[index:], token_list)

            # In this context the function is considered an LTOKEN
            if string[index] == ARG_OPEN:
                index += lex_args(string[index:], token_list,
                                  arg_tokens=(LT.FUNCTION_ARGS, LT.FUNCTION, LT.FUNCTION_ARGS_END))
                # Add 1 because you are breaking
                index += 1

        elif c in CONTEXT_TOKENS:
            token_list.append((LT.CONTEXT_TOKEN, c))
            index += 1

        elif c == CONDITION_TOKEN:
            # index += 1  # Skip the CONDITION_TOKEN
            index += lex_condition(string[index:], token_list)

        elif c == RESULT_TOKEN:
            token_list.append((LT.RESULT, None))
            index += 1

        elif c == LINE_BREAK:
            index += 1
            token_list.append((LT.RESULT_END, None))
            index += lex_linebreak(string[index:], token_list)
            break

        elif c == " ":
            index += 1

        else:
            raise SyntaxError(f"Character '{c}' is not valid token start or rule component.")

    return index
