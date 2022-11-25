from compiler.l_compiler import l_compile
from lexer.lex import lex
from lexer.static import ARGV_DEBUG, ARGV_WARNING
from lexer.token_compactor import token_compactor
import sys


if __name__ == '__main__':
    # Change LTOKEN token to have
    # (LT.LTOKEN, [
    #   (LT.NAME, 'A'),
    #   (LT.ARGS, [(LT.ARG, 'b')])
    # ]
    # So include name and args into the token itself

    from pprint import pprint
    sys.argv += [ARGV_WARNING, ARGV_DEBUG]
    test_string = open("test/test.l", encoding="utf-8").read()

    # Lex the file
    tk = lex(test_string)

    # Compact tokens
    _compacted_tokens = token_compactor(tk)

    pprint(_compacted_tokens)
    l_compile(_compacted_tokens)
