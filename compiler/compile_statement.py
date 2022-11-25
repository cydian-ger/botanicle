from typing import List, Tuple, Any, Optional, Dict

from common.LWarning import LWarning
from compiler.bottle import Bottle
from compiler.compile_error import Compile_Error
from compiler.statement.define import define
from compiler.statement.expose import expose
from compiler.statement.ignore import ignore
from compiler.statement.group import group
from lexer.LT import LT
from lexer.static import KW


def compile_statement(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    info: Optional[Dict[str, Any]] = token_list.pop(0)[1]

    try:
        # for token, content in token_list:
        #     if token not in {LT.KEYWORD, LT.ARGS, LT.NAME, LT.VALUE, LT.PATH}:
        #         raise Compile_Error(f"Token {token} is not a valid statement token.", info, SyntaxError)
        # Check if the args are valid

        statement = token_list.pop(0)[1]

        match statement:
            case KW.define:
                define(token_list, bottle)

            case KW.group:
                group(token_list, bottle)

            case KW.ignore:
                ignore(token_list, bottle)

            case KW.expose:
                expose(token_list, bottle)

            case _:
                LWarning(f"Keyword '{statement}' not implemented yet.").throw()

    except Compile_Error as e:
        raise e

    except Exception as e:
        raise Compile_Error(e.args[0], info, e)
    # Put info here

