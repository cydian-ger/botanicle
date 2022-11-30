from typing import List, Tuple, Any

from common.LWarning import LWarning
from compiler.lcompiler.bottle import Bottle
from compiler.lcompiler.statement.define import define
from compiler.lcompiler.statement.expose import expose
from compiler.lcompiler.statement.ignore import ignore
from compiler.lcompiler.statement.group import group
from compiler.lcompiler.statement.include import include
from compiler.lexer.LT import LT
from compiler.lexer.static import KW


def compile_statement(token_list: List[Tuple[LT, Any, Tuple[int, int]]], bottle: Bottle,
                      line_token: Tuple[LT, Any, Tuple[int, int]]):
    # for token, content in token_list:
    #     if token not in {LT.KEYWORD, LT.ARGS, LT.NAME, LT.VALUE, LT.PATH}:
    #         raise Compile_Error(f"Token {token} is not a valid statement token.", info, SyntaxError)
    # Check if the args are valid

    statement = token_list.pop(0)[1]

    match statement:
        case KW.define:
            define(token_list, bottle, line_token)

        case KW.group:
            group(token_list, bottle, line_token)

        case KW.ignore:
            ignore(token_list, bottle, line_token)

        case KW.expose:
            expose(token_list, bottle, line_token)

        case KW.include:
            include(token_list, bottle, line_token)

        case _:
            LWarning(f"Keyword '{statement}' not implemented yet.").throw()
