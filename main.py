from pprint import pprint
from lexer.lex import lex
from lexer.token_compactor import token_compactor
import sys

if __name__ == '__main__':
    sys.argv.append("-debug")
    test_string = open("test/test.l", encoding="utf-8").read()

    # e.g. "b == a"
    tk = lex(test_string)
    pprint(token_compactor(tk))
