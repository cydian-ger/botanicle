from typing import List, Tuple, Any, Union

from compiler.Lglobal import lraise
from compiler.lcompiler.bottle import Bottle
from compiler.lcompiler.compile_rule import compile_rule
from compiler.lcompiler.compile_statement import compile_statement
from compiler.lexer.LT import LT


# This compiles a single file
from compiler.lexer.static import ASSIGNMENT_TOKEN, START_RULE


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

    if bottle.start is None:
        lraise(KeyError(f"There is no rule defined with the assignment {ASSIGNMENT_TOKEN + START_RULE}"),
               err_pos=(0, 0))
    return bottle
