import re

from compiler.lexer.static import RESULT_TOKEN


def lint(string: str):
    # Replace characters
    string = re.sub("->", RESULT_TOKEN, string)

    # Append a new line at the end
    # Because else while(index < len(string)) fails at bad times
    if string[-1] != "\n":
        string += "\n"

    # Remove trailing spaces
    lines = string.split("\n")
    lines = [line.rstrip(" ") for line in lines]

    string = "\n".join(lines)
    return string
