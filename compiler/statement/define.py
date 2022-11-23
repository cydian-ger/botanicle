from typing import List, Tuple, Any
from compiler.bottle import Bottle
from compiler.compile_error import Compile_Error
from lexer.LT import LT
from lexer.static import KW


def define(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    # CHECK FORM
    # define: [name alias value]

    if len(token_list) != 3:
        raise SyntaxError("")

    if not token_list[0][0] == LT.NAME:
        raise ValueError("First argument of define has to be a variable name.")

    if not token_list[1][0] == LT.KEYWORD and token_list[1][1] == KW.alias:
        raise SyntaxError(f"Second argument of define has to be {KW.alias}")

    if not token_list[2][0] == LT.VALUE:
        raise ValueError(f"Third argument of define has to be a numeric value")

    # Form is asserted as correct now
    variable_name = token_list[0][1]

    try:
        variable_value = float(token_list[2][1])
    except Exception as e:
        raise ValueError(f"The value of a variable has to be a valid floating point number.")

    # Check if value is already in bottle
    # Add value to bottle

    return
