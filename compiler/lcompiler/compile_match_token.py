from common.datatypes import Name, Value_List, Token
from common.datatypes.LMatch import LMatch
from common.datatypes.lgroup import Group
from compiler.Lglobal import lraise
from compiler.lcompiler.bottle import Bottle
from compiler.lexer.LT import LT


def compile_lmatch(name: str, args, bottle: Bottle, token_index):
    token_name = Token(name, token_index)

    # If it is a group use the group instead
    if name in bottle.match_groups.keys():
        token_name = Group(token_name, bottle.match_groups[token_name])

    token_args = Value_List()
    token_args.set_type(Name)
    # Add every argument
    for arg_t, arg_v, arg_i in args:
        if arg_t == LT.ARG or arg_t == LT.EXPR:
            token_args.append(Name(arg_v))  # had ,arg_i)

        elif arg_t == LT.FUNCTION:
            # Load function
            lraise(NotImplementedError("Functions as arguments in LTokens are not supported yet"), arg_i)

        else:
            lraise(SyntaxError(f"Invalid Argument Type for Token: {arg_t}."), arg_i)

    return LMatch(token_name, token_args)
