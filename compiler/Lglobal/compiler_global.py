import sys

Compiler = sys.modules[__name__]

Compiler.string = None
Compiler.err_padding = None


def init_compiler(string: str):
    if Compiler.string is None:
        Compiler.string = string
        Compiler.err_padding = 2
    else:
        raise RuntimeError("Variable already defined")
