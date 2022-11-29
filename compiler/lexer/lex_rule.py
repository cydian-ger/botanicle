from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.lex_args import lex_args
from compiler.lexer.lex_assignment import lex_assignment
from compiler.lexer.lex_error import LexError
from compiler.lexer.lex_function import lex_function
from compiler.lexer.lex_linebreak import lex_linebreak
from compiler.lexer.lex_ltoken import lex_ltoken
from compiler.lexer.lex_condition import lex_condition
from compiler.lexer.static import VALID_RULE_LTOKENS, CONTEXT_TOKENS, CONDITION_TOKEN, RESULT_TOKEN, LINE_BREAK, \
    ASSIGNMENT_TOKEN, FUNCTION_TOKEN, ARG_OPEN
from compiler.compiler_global import char


def lex_rule(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0
    result_token: bool = False
    condition_token: bool = False

    while index < len(string):
        c = string[index]

        if c in VALID_RULE_LTOKENS:
            index += lex_ltoken(string[index:], token_list)

        elif c == ASSIGNMENT_TOKEN:
            if index > 0:
                raise LexError(f"Assignment operator '{ASSIGNMENT_TOKEN}' must be at the start of a line",
                               string[index:], SyntaxError)
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
            token_list.append((LT.CONTEXT_TOKEN, c, char(string[index + 1:])))
            index += 1

        elif c == CONDITION_TOKEN:
            if condition_token:
                raise LexError("Condition token can not appear more than once in a rule", string[index:], SyntaxError)
            condition_token = True

            index += lex_condition(string[index:], token_list)

        elif c == RESULT_TOKEN:
            if result_token:
                raise LexError("Result token can not appear more than once in a rule.", string[index:], SyntaxError)
            result_token = True

            token_list.append((LT.RESULT, None, char(string[index:])))
            index += 1

        elif c == LINE_BREAK:
            index += 1

            if result_token:
                token_list.append((LT.RESULT_END, None, char(string[index:])))

            index += lex_linebreak(string[index:], token_list)
            break

        elif c == " ":
            index += 1

        else:
            raise LexError(f"Character '{c}' is not a valid LToken / rule component.",
                           string[index:], SyntaxError)

    return index