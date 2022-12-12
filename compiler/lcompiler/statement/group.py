import sys

from common.env import env_args
from compiler.lexer.LT import LT
from compiler.lcompiler.bottle import Bottle
from typing import List, Tuple, Any
from common.datatypes import Value_List, Token
from compiler.lexer.static import KW, SPECIAL_AXIOMS, ARGV_WARNING
from compiler.Lglobal import lraise, lwarn


def append(ltk, group_values, name, token):
    if ltk not in group_values:
        group_values.append(ltk)
    else:
        lwarn(SyntaxWarning(f"Argument '{ltk}'"
                            f" is included multiple times in '{name}: "
                            f"({', '.join([str(t_arg[1]) for t_arg in token])})'"))


def group(token_list: List[Tuple[LT, Any, Tuple[int, int]]],
          bottle: Bottle, parent_token: Tuple[LT, Any, Tuple[int, int]]):
    # Check form
    # group: [name alias value_list[]]

    if len(token_list) != 3:
        lraise(SyntaxError(f"Ignore takes 3 Argument. {len(token_list)} were provided"),
               parent_token[2])

    if not token_list[0][0] == LT.NAME:
        lraise(ValueError("First argument has to be a variable name."), token_list[0][2])

    if not token_list[1][0] == LT.KEYWORD and token_list[1][1] == KW.alias:
        lraise(SyntaxError(f"Second argument has to be {KW.alias}"), token_list[1][2])

    if not token_list[2][0] == LT.ARGS:
        lraise(ValueError(f"Third argument has to be an argument list."), token_list[2][2])

    for arg in token_list[2][1]:
        if not arg[0] == LT.ARG:
            lraise(ValueError(f"Arguments inside the third argument have to be ARGS type. "
                              f"Argument '{arg[1]}' was '{arg[0]}' instead."), arg[2])

    if token_list[0][1] not in SPECIAL_AXIOMS:
        lraise(SyntaxError(f"Group name has to be a special Axiom character. '{SPECIAL_AXIOMS}'"), token_list[0][2])

    group_name = Token(token_list[0][1], token_list[0][2])

    # Check if already in group names
    if bottle.token_already_exists(group_name):
        lraise(KeyError(f"Group '{group_name}' is already defined."), token_list[0][2])

    group_values = Value_List()
    group_values.set_type(Token)

    for argument in token_list[2][1]:
        ltoken = Token(argument[1], token_list[2][2])

        # If the l token is already a
        if str(ltoken) in bottle.match_groups:
            for bottle_ltoken in bottle.match_groups[ltoken]:
                append(bottle_ltoken, group_values, group_name, token_list[2][1])

        # If the token is not defined already but is a special axiom
        elif str(ltoken) in SPECIAL_AXIOMS:
            lraise(ReferenceError(f"LToken '{ltoken}' is undefined. Since it is a special LToken it has to be "
                                  f"defined as a capture group to be included."), token_list[2][2])

        else:
            append(Token(argument[1], token_list[2][2]), group_values, group_name, token_list[2][1])

    # Warn if the group_values are already in the bottle under a different name
    if env_args.__contains__(ARGV_WARNING):
        for name, values in bottle.match_groups.items():
            if values == group_values:
                lwarn(Warning(f"Group '{group_name}: ({', '.join([str(g_value) for g_value in group_values])})"
                              f"' is already in the bottle: "
                              f"'{name}: ({', '.join([str(value) for value in values])})'"))
    bottle.match_groups[group_name] = group_values

    return
