from typing import List, Tuple, Any
from compiler.lcompiler.bottle import Bottle
from common.datatypes import Token, Name
from compiler.lexer.LT import LT
from compiler.lexer.static import KW
from compiler.Lglobal import lraise


def include(token_list: List[Tuple[LT, Any, Tuple[int, int]]],
           bottle: Bottle, parent_token: Tuple[LT, Any, Tuple[int, int]]):
    # CHECK FORM
    # include: [path alias token]

    if len(token_list) != 3:
        lraise(SyntaxError(f"Include takes 3 Arguments. {len(token_list)} were provided."), parent_token[2])

    if not token_list[0][0] == LT.PATH:
        lraise(ValueError("First argument has to be a path."), token_list[0][2])

    if not token_list[1][0] == LT.KEYWORD or not token_list[1][1] == KW.alias:
        lraise(ValueError(f"Second argument has to be keyword: '{KW.alias}'"), token_list[1][1])

    if not token_list[2][0] == LT.NAME:
        lraise(ValueError(f"Third argument has to be a token"), token_list[2][2])

    path = Name(token_list[0][1], token_list[0][2])
    ltoken = Token(token_list[2][1], token_list[2][2])

    if bottle.token_already_exists(ltoken):
        lraise(KeyError(f"LToken already defined"), token_list[2][2])

    bottle.frame.linked_files[ltoken] = path
    return
