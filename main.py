import sys

from common.common_names import COMPILED_FORMAT
from compiler.Lcompile_file import compile_file
from compiler.lcompiler.bottle import Bottle
import pickle
from pprint import pprint

from compiler.lexer.static import ARGV_DEBUG, ARGV_WARNING

if __name__ == '__main__':
    # BUD: Bottle of U-- Data
    sys.argv.append(ARGV_DEBUG)
    sys.argv.append(ARGV_WARNING)
    NAME = "test/test"
    compile_file(NAME)

    f = open(NAME + COMPILED_FORMAT, 'rb')
    y: Bottle = pickle.load(f)
    f.close()
    pprint(y)
