from typing import List, Tuple, Any
from lexer.LT import LT


def lex_reference(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    # Maybe call it a reference or something
    # @testline

    # Index is 1 to skip the REFERENCE TOKEN
    index = 1
    assignment_call = ""

    while index < len(string):
        c = string[index]

        if not c.isalpha():
            break

        assignment_call += c
        index += 1

    token_list.append((LT.REFERENCE, assignment_call))

    return index
