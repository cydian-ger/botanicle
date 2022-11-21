from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.lex_error import LexError
from lexer.static import SPACE, ASSIGNMENT_TOKEN


def lex_assignment(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    index = 0
    assignment = ""

    while index < len(string):
        c = string[index]

        if c == ASSIGNMENT_TOKEN:
            if index > 0:
                raise LexError(f"Assignment Token {ASSIGNMENT_TOKEN} can not be part of the assignement name",
                               string[index:], SyntaxError)  # Can't contain a ASSIGNMENT TOKEN after the initial one
            # Else it skips the first token
            index += 1

        elif not c.isalpha():  # " "
            break

        else:
            assignment += c
            index += 1

    # TODO
    # CHECK NAMING CONVENTION FOR THE ASSIGNMENT

    if len(assignment) == 0:
        raise LexError(f"Assignment Token '{ASSIGNMENT_TOKEN}' has to be followed by at least 1 character",
                       string[index:], SyntaxError)

    token_list.append((LT.ASSIGNMENT, assignment))
    return index
