from typing import List, Tuple, Any
from compiler.bottle import Bottle
from common.datatypes import Value_List, Token
from compiler.lexer.LT import LT
from compiler.compiler_global import lraise


def ignore(token_list: List[Tuple[LT, Any, Tuple[int, int]]],
           bottle: Bottle, parent_token: Tuple[LT, Any, Tuple[int, int]]):
    # CHECK FORM
    # ignore [[Value List[LToken]]]

    if len(token_list) != 1:
        lraise(SyntaxError(f"Ignore takes 1 Argument. {len(token_list)} were provided"), parent_token[2])

    if not token_list[0][0] == LT.ARGS:
        lraise(ValueError("First argument has to be a list of tokens."), token_list[0][2])

    ignore_list = Value_List()
    ignore_list.set_type(Token)

    for _, ltoken, __ in token_list[0][1]:
        ignore_list.append(Token(ltoken))

    if not not bottle.context_ignore:
        lraise(NameError(f"Ignore can not be defined twice."), parent_token[2])

    # pass
    for value in ignore_list:
        bottle.context_ignore.add(value)

    return
