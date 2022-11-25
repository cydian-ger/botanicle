from typing import List, Tuple, Any
from compiler.bottle import Bottle
from datatypes import Token, Name
from lexer.LT import LT
from lexer.static import KW


def include(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    # CHECK FORM
    # include: [path alias token]

    if len(token_list) != 3:
        raise SyntaxError(f"Include takes 3 Arguments. {len(token_list)} were provided.")

    if not token_list[0][0] == LT.PATH:
        raise ValueError("First argument has to be a path.")

    if not token_list[1][0] == LT.KEYWORD or not token_list[1][1] == KW.alias:
        raise ValueError(f"Second argument has to be keyword: '{KW.alias}'")

    if not token_list[2][0] == LT.NAME:
        raise ValueError(f"Third argument has to be a token")

    path = Name(token_list[0][1])
    ltoken = Token(token_list[2][1])

    if bottle.token_already_exists(ltoken):
        raise KeyError(f"LToken already defined")

    bottle.frame.linked_files[ltoken] = path
    return
