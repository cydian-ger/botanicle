from typing import List, Tuple, Any, Union

from compiler.bottle import Bottle
from compiler.compile_rule import compile_rule
from compiler.compile_statement import compile_statement
from compiler.lexer.LT import LT


# This compiles a single file
def l_compile(token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]):
    bottle: Bottle = Bottle()

    for line_token in token_list:
        token, content, token_index = line_token
        content: List[Tuple[LT, Any, Tuple[int, int]]]

        match token:
            case LT.STATEMENT:
                compile_statement(content, bottle, line_token)

            case LT.RULE:
                compile_rule(content, bottle, line_token)

            case LT.COMMENT:
                # Comments are skipped for now
                continue

    return bottle
