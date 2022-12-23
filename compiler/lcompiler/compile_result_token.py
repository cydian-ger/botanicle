from typing import Dict

from common.datatypes import Value_List, Expression, Name, Token
from common.datatypes.LResult import LResult
from compiler.Lglobal import lraise
from compiler.lcompiler.bottle import Bottle
from compiler.lexer.LT import LT
from compiler.lexer.static import GENERIC


def compile_result_token(name, args, bottle: Bottle, kwargs: Dict, token_index):
    token_name = Token(name, token_index)
    token_args = Value_List()
    token_args.set_type(Expression)

    is_group = False
    # Check if the result is a generic
    if name in bottle.match_groups.keys() or name == GENERIC:
        is_group = True

    # TODO change it to be like in match token
    # Check generics in compile_rule after

    for arg_type, arg_value, arg_index in args:
        if arg_type == LT.ARG or arg_type == LT.EXPR:
            token_args.append(Expression(arg_value, arg_index, **kwargs))

        elif arg_type == LT.FUNCTION:
            # Load function
            lraise(NotImplementedError("Functions as arguments in LResults are not supported yet"), arg_index)

        else:
            lraise(SyntaxError(f"Invalid Argument Type for LResult: {arg_type}."), arg_index)

    return LResult(token_name, token_args, is_group)
