import sys
from lexer.LT import LT
from compiler.bottle import Bottle
from typing import List, Tuple, Any
from common.LWarning import LWarning
from datatypes import Value_List, Token
from lexer.static import KW, SPECIAL_AXIOMS, ARGV_WARNING


def append(ltk, group_values, name):
    if ltk not in group_values:
        group_values.append(ltk)
    else:
        if sys.argv.__contains__(ARGV_WARNING):
            LWarning(f"Argument '{ltk}'"
                     f" is included multiple times in '{name}: ({', '.join(group_values)})'").throw()


def group(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    # Check form
    # group: [name alias value_list[]]

    if len(token_list) != 3:
        raise SyntaxError(f"Ignore takes 3 Argument. {len(token_list)} were provided")

    if not token_list[0][0] == LT.NAME:
        raise ValueError("First argument has to be a variable name.")

    if not token_list[1][0] == LT.KEYWORD and token_list[1][1] == KW.alias:
        raise SyntaxError(f"Second argument has to be {KW.alias}")

    if not token_list[2][0] == LT.ARGS:
        raise ValueError(f"Third argument has to be an argument list.")

    for arg in token_list[2][1]:
        if not arg[0] == LT.ARG:
            raise ValueError("Arguments inside the third argument have to be ARGS type.")

    group_name = Token(token_list[0][1])

    # Check if already in group names
    if bottle.token_already_exists(group_name):
        raise KeyError(f"Group '{group_name}' is already defined.")

    group_values = Value_List()
    group_values.set_type(Token)

    for argument in token_list[2][1]:
        ltoken = Token(argument[1])

        # If the l token is already a
        if ltoken in bottle.groups:
            for bottle_ltoken in bottle.groups[ltoken]:
                append(bottle_ltoken, group_values, group_name)

        # If the token is not defined already but is a special axiom
        elif ltoken in SPECIAL_AXIOMS:
            raise ReferenceError(f"LToken '{ltoken}' is undefined. Since it is a special LToken it has to be "
                                 f"defined as a capture group to be included.")

        else:
            append(Token(argument[1]), group_values, group_name)

    # Warn if the group_values are already in the bottle under a different name
    if sys.argv.__contains__(ARGV_WARNING):
        for name, values in bottle.groups.items():
            if values == group_values:
                LWarning(f"Group '{group_name}: ({', '.join(group_values)})' is already in the bottle: "
                         f"''{name}: ({', '.join(values)})''").throw()

    bottle.groups[group_name] = group_values

    return
