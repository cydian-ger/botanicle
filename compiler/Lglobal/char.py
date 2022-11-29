from compiler.Lglobal import Compiler


def char(str_left: str):
    # str_left is the amount of string that is left
    return len(Compiler.string) - len(str_left)