from typing import List, Tuple, Any, Optional, Dict
from compiler.bottle import Bottle
from compiler.compile_error import Compile_Error
from compiler.statement.define import define
from lexer.LT import LT
from lexer.static import KW
from colorama import Fore, Style


def compile_statement(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    info: Optional[Dict[str, Any]] = token_list.pop(0)[1]

    try:
        for token, content in token_list:
            if token not in {LT.KEYWORD, LT.ARGS, LT.NAME, LT.VALUE, LT.PATH}:
                raise Compile_Error(f"Token {token} is not a valid statement token.", info, SyntaxError)
                # Check if the args are valid

        statement = token_list.pop(0)[1]

        match statement:
            case KW.define:
                define(token_list, bottle)

    except Exception as e:
        raise Compile_Error(e.args[0], info, e)
    # Put info here

