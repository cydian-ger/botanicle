from typing import List, Tuple, Any
from compiler.lcompiler.bottle import Bottle
from common.datatypes import Value_List, Name, Expression
from compiler.lexer.LT import LT
from compiler.lexer.static import KW
from compiler.Lglobal import lraise


def expose(token_list: List[Tuple[LT, Any, Tuple[int, int]]],
           bottle: Bottle, parent_token: Tuple[LT, Any, Tuple[int, int]]):
    # Check form
    # group: [name alias value_list[]]

    if len(token_list) != 1 and len(token_list) != 3:
        lraise(SyntaxError(f"Ignore takes 3 or 1 Argument. {len(token_list)} were provided"),
               parent_token[2])

    if not token_list[0][0] == LT.ARGS:
        lraise(ValueError("First argument has to be a a list of variable names."), token_list[2][2])

    value_list: Value_List[Name] = Value_List()
    value_list.set_type(Name)

    for argument in token_list[0][1]:
        name = Name(argument[1])
        value_list.append(name)

    if bottle.frame.exposed_variables is not None:
        lraise(ValueError("Exposed variables are already defined."), parent_token[2])

    bottle.frame.exposed_variables = value_list

    if len(token_list) == 1:
        return

    if not token_list[1][0] == LT.KEYWORD and not token_list[1][1] == KW.lwith:
        lraise(SyntaxError(f"Second argument has to be keyword: '{KW.lwith}'"), token_list[1][2])

    if not token_list[2][0] == LT.ARGS:
        lraise(ValueError("Third argument has to be a a list of variable names."), token_list[2][2])

    condition_list: Value_List[Expression] = Value_List()
    condition_list.set_type(Expression)

    for argument in token_list[2][1]:
        expr = Expression(argument[1], token_list[2][2])
        condition_list.append(expr)

    if bottle.frame.exposing_conditions is not None:
        lraise(ValueError("Exposed variable conditions are already defined."), parent_token[2])

    bottle.frame.exposing_conditions = condition_list
