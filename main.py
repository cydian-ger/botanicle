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
    # Implement ? as the way to retrieve a generic match
    # ? <Match>
    # Allow a group match / generic match to be retrieved in context so:
    # ? < * > ? : -> ?
    # if * matches an A
    # then during that match the rule is
    # A < * > A : -> A
    # This avoids cluster fuck from using groups and retrieving
    # [Match Retrieval in LResult]: Done
    # [Match Retrieval in LMatch]: -

    # Add step wise iterating

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

    production(NAME, {"max_iter": 7})
