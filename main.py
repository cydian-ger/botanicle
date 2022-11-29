import sys

from compiler.Lglobal import init_compiler
from compiler.l_compiler import l_compile
from compiler.lexer.lex import lex
from compiler.lexer.static import ARGV_DEBUG, ARGV_WARNING
from compiler.lexer.token_compactor import token_compactor

if __name__ == '__main__':
    from pprint import pprint

    sys.argv.append(ARGV_WARNING)
    sys.argv.append(ARGV_DEBUG)

    test_string = open("test/test.l", encoding="utf-8").read()
    init_compiler(test_string)

    # Lex the file
    tk = lex(test_string)

    # Compact tokens
    _compacted_tokens = token_compactor(tk)

    # pprint(_compacted_tokens, width=120)
    bottle = l_compile(_compacted_tokens)
    pprint(bottle)

    # TODO
