from compiler.l_compiler import l_compile
from lexer.lex import lex
from lexer.token_compactor import token_compactor
import sys

if __name__ == '__main__':
    sys.argv.append("-debug")
    test_string = open("test/test.l", encoding="utf-8").read()

    # e.g. "b == a"
    # ERROR may be because the error is on the first character of the line,
    tk = lex(test_string)
    # pprint(token_compactor(tk))
    l_compile(token_compactor(tk))
