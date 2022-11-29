from typing import List, Tuple, Any
from compiler.bottle import Bottle
from common.datatypes import Value
from compiler.lexer.LT import LT
from compiler.lexer.static import KW
from compiler.Lglobal import lraise


def define(token_list: List[Tuple[LT, Any, Tuple[int, int]]],
           bottle: Bottle, parent_token: Tuple[LT, Any, Tuple[int, int]]):
    # CHECK FORM
    # define: [name alias value]

    if len(token_list) != 3:
        lraise(SyntaxError(f"Define takes 3 Argument. {len(token_list)} were provided"), parent_token[2])

    if not token_list[0][0] == LT.NAME:
        lraise(ValueError("First argument has to be a variable name."), token_list[0][2])

    if not token_list[1][0] == LT.KEYWORD and token_list[1][1] == KW.alias:
        lraise(SyntaxError(f"Second argument has to be {KW.alias}"), token_list[1][2])

    if not token_list[2][0] == LT.VALUE:
        lraise(ValueError(f"Third argument has to be a numeric value"), token_list[2][2])

    # Form is asserted as correct now
    variable_name = token_list[0][1]

    try:
        variable_value = Value(token_list[2][1])
    except ValueError:
        lraise(ValueError(f"The value of a variable has to be a valid floating point number."), token_list[2][2])
        # For editor only. This has no use in runtime
        raise None

    # Check if value is already in bottle
    if variable_name in bottle.variables:
        lraise(KeyError(f"Variable with name {variable_name} is already defined."), token_list[0][2])
    # Add value to bottle
    bottle.add_variable(variable_name, variable_value)
    return
