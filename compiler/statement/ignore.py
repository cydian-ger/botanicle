from typing import List, Tuple, Any
from compiler.bottle import Bottle
from datatypes import Value_List, Token
from lexer.LT import LT


def ignore(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    # CHECK FORM
    # ignore [[Value List[LToken]]]

    if len(token_list) != 1:
        raise SyntaxError(f"Ignore takes 1 Argument. {len(token_list)} were provided")

    if not token_list[0][0] == LT.ARGS:
        raise ValueError("First argument has to be a list of tokens.")

    ignore_list = Value_List()
    ignore_list.set_type(Token)

    for _, ltoken in token_list[0][1]:
        ignore_list.append(Token(ltoken))

    if not not bottle.context_ignore:
        raise NameError(f"Ignore can not be defined twice.")

    # pass
    for value in ignore_list:
        bottle.context_ignore.add(value)

    return
