import pickle
from typing import IO
from compiler.Lglobal import init_compiler
from compiler.lcompiler.l_compiler import l_compile
from compiler.lexer.lex import lex
from compiler.lexer.token_compactor import token_compactor


def compile_file(file: IO, name: str):
    # Read the file and init the compiler
    test_string = file.read()
    init_compiler(test_string)

    # Lex the file
    tk = lex(test_string)

    # Compact tokens
    _compacted_tokens = token_compactor(tk)

    # Bake the tokens into a bottle
    bottle = l_compile(_compacted_tokens)

    f = open(name, 'wb')
    pickle.dump(bottle, f)
    f.close()
    return
