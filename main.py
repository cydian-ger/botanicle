from common.common_names import COMPILED_FORMAT
from common.env import env_args
from compiler.Lcompile_file import compile_file
from compiler.lcompiler.bottle import Bottle
import cloudpickle
from pprint import pprint

from compiler.lexer.static import ARGV_DEBUG, ARGV_WARNING, ARGV_LINT
from production.Lproduction import production

if __name__ == '__main__':
    # TODO
    # Think up a proper way of how the generics are handled and else the matches loaded
    # with the correct Token name

    # TODO
    # Implement check for named results
    # Go through every reference onto a named_result:
    # If there is a generic match, check if the generic is resolved
    # Maybe have sth like '?' if you have 1 rule with match group and the other with match
    # Maybe overwork the system to just have '?' Access the generic match in the result
    # ? = Match Token. Whatever LToken was matched ? receives that signature. ?(a, ...)
    # ? has to match the amount of arguments in the match.
    # ? can appear in any result (because even the normal match is just a match)
    # e.g. A < B > C : -> ??  would result in BB. (Maybe give a warning here)

    # DO NOT ALLOW GROUP MATCH RETRIEVAL IN CONTEXT (for now)
    # That would just be too confusing, I don't see a use case there.
    # Say no to clutter-ware

    # BUD: Bottle of U-- Data
    env_args.append(ARGV_LINT)
    env_args.append(ARGV_DEBUG)
    env_args.append(ARGV_WARNING)
    NAME = "testing/test"
    compile_file(NAME)

    f = open(NAME + COMPILED_FORMAT, 'rb')
    y: Bottle = cloudpickle.load(f)
    f.close()
    pprint(y)

    production(NAME)
