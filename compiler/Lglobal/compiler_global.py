import sys
from common.env import env_args
from compiler.lexer.static import ARGV_TEST

Compiler = sys.modules[__name__]

Compiler.string = None
Compiler.err_padding = None


def init_compiler(string: str):
    if Compiler.string is not None:
        raise RuntimeError("Variable already defined")

    Compiler.string = string
    Compiler.err_padding = 2


def reset_compiler():
    Compiler.string = None
    Compiler.err_padding = None


if env_args.__contains__(ARGV_TEST):
    init_compiler(" ")
