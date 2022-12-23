import re


def lint(string: str):
    string = re.sub("->", "→", string)

    # Because else while(index < len(string)) fails at bad times
    if string[-1] != "\n":
        string += "\n"
    return string
