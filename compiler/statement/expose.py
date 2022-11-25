from typing import List, Tuple, Any
from compiler.bottle import Bottle
from datatypes import Value_List, Name, Expression
from lexer.LT import LT
from lexer.static import KW


def expose(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    # Check form
    # group: [name alias value_list[]]

    if len(token_list) != 1 and len(token_list) != 3:
        raise SyntaxError(f"Ignore takes 3 or 1 Argument. {len(token_list)} were provided")

    if not token_list[0][0] == LT.ARGS:
        raise ValueError("First argument has to be a a list of variable names.")

    value_list: Value_List[Name] = Value_List()
    value_list.set_type(Name)

    for argument in token_list[0][1]:
        name = Name(argument[1])
        value_list.append(name)

    if bottle.frame.exposed_variables is not None:
        raise ValueError("Exposed variables are already defined.")

    bottle.frame.exposed_variables = value_list

    if len(token_list) == 1:
        return

    if not token_list[1][0] == LT.KEYWORD and not token_list[1][1] == KW.lwith:
        raise SyntaxError(f"Second argument has to be keyword: '{KW.lwith}'")

    if not token_list[2][0] == LT.ARGS:
        raise ValueError("Third argument has to be a a list of variable names.")

    condition_list: Value_List[Expression] = Value_List()
    condition_list.set_type(Expression)

    for argument in token_list[2][1]:
        expr = Expression(argument[1])
        condition_list.append(expr)

    if bottle.frame.exposing_conditions is not None:
        raise ValueError("Exposed variable conditions are already defined.")

    bottle.frame.exposing_conditions = condition_list