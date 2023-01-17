import cloudpickle
from common.common_names import EDITOR_FORMAT, COMPILED_FORMAT
from common.env import env_args
from compiler.Lglobal import init_compiler
from compiler.lcompiler.l_compiler import l_compile
from compiler.lexer.lex import lex
from compiler.lexer.static import ARGV_LINT
from compiler.lexer.token_compactor import token_compactor
from compiler.lint.lint import lint


def compile_file(name: str):
    ENCODING = "utf-8"
    file = open(name + EDITOR_FORMAT, encoding=ENCODING)
    # Read the file and init the compiler

    string = file.read()

    # Lint the file.
    if env_args.__contains__(ARGV_LINT):
        string = lint(string)
        file.close()
        file = open(name + EDITOR_FORMAT, "w", encoding=ENCODING)
        file.write(string)
    file.close()

    init_compiler(string)

    # Lex the file
    tk = lex(string)

    # Compact tokens
    _compacted_tokens = token_compactor(tk)
    # from pprint import pprint
    # pprint(_compacted_tokens)

    # Bake the tokens into a bottle
    bottle = l_compile(_compacted_tokens)

    f = open(name + COMPILED_FORMAT, 'wb')
    cloudpickle.dump(bottle, f)
    f.close()
    return bottle
