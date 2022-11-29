from typing import List, Tuple, Any, Optional, Dict

from common.LWarning import LWarning
from compiler.bottle import Bottle
from compiler.compile_error import Compile_Error
from compiler.statement.define import define
from compiler.statement.expose import expose
from compiler.statement.ignore import ignore
from compiler.statement.group import group
from compiler.statement.include import include
from compiler.lexer.LT import LT
from compiler.lexer.static import KW


def compile_statement(token_list: List[Tuple[LT, Any, Tuple[int, int]]], bottle: Bottle,
                      line_token: Tuple[LT, Any, Tuple[int, int]]):
    info: Optional[Dict[str, Any]] = token_list.pop(0)[1]

    try:
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

    except Compile_Error as e:
        raise e

    except Exception as e:
        if len(e.args) > 0:
            raise Compile_Error(e.args[0], info, e)
        else:
            raise Compile_Error("ERROR MSG MISSING", info, e)
    # Put info here
