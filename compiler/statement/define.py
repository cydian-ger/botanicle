from typing import List, Tuple, Any
from compiler.bottle import Bottle
from datatypes import Value
from lexer.LT import LT
from lexer.static import KW


def define(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    # CHECK FORM
    # define: [name alias value]

    if len(token_list) != 3:
        raise SyntaxError(f"Ignore takes 3 Argument. {len(token_list)} were provided")

    if not token_list[0][0] == LT.NAME:
        raise ValueError("First argument has to be a variable name.")

    if not token_list[1][0] == LT.KEYWORD and token_list[1][1] == KW.alias:
        raise SyntaxError(f"Second argument has to be {KW.alias}")

    if not token_list[2][0] == LT.VALUE:
        raise ValueError(f"Third argument has to be a numeric value")

    # Form is asserted as correct now
    variable_name = token_list[0][1]

    try:
        variable_value = Value(token_list[2][1])
    except ValueError:
        raise ValueError(f"The value of a variable has to be a valid floating point number.")

    # Check if value is already in bottle
    # Add value to bottle

    bottle.add_variable(variable_name, variable_value)
    return
