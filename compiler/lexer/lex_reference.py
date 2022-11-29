from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.compiler_global import char


def lex_reference(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
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

    token_list.append((LT.REFERENCE, assignment_call, char(string[index:])))

    return index
