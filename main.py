import sys

from common.common_names import COMPILED_FORMAT
from compiler.Lcompile_file import compile_file
from compiler.lcompiler.bottle import Bottle
import pickle
from pprint import pprint

from compiler.lexer.static import ARGV_DEBUG, ARGV_WARNING
from production.Lproduction import production

if __name__ == '__main__':
    # TODO Rule index is incorrect
    # Problem seems to be in the lexing and token_index part
    # Possibly related to the assignment lexing.
    # Appeared due to the Initial axiom being absent. (probably un-related though)

    # TODO: Implement generics and groups in matches
    # if group in result, group has to be in match (same goes for generic)
    # Have the rule matches allow groups and generics.

    # BUD: Bottle of U-- Data
    sys.argv.append(ARGV_DEBUG)
    sys.argv.append(ARGV_WARNING)
    NAME = "test/test"
    compile_file(NAME)

    f = open(NAME + COMPILED_FORMAT, 'rb')
    y: Bottle = pickle.load(f)
    f.close()
    pprint(y)

    production(NAME)
