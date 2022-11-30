from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.static import SPACE, ASSIGNMENT_TOKEN, LINE_BREAK
from compiler.Lglobal import char, lraise


def lex_assignment(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0
    assignment = ""

    while index < len(string):
        c = string[index]

        if c == ASSIGNMENT_TOKEN:
            if index > 0:
                lraise(SyntaxError(f"Assignment Token {ASSIGNMENT_TOKEN} can not be part of the assignment name"),
                       char(string[index:]))  # Can't contain a ASSIGNMENT TOKEN after the initial one
            # Else it skips the first token
            index += 1

        elif c == SPACE:
            break

        elif c == LINE_BREAK:
            lraise(SyntaxError(f"Assignment can not be followed by a line break."), char(string[index:]))

        elif not c.isalnum():  # " "
            lraise(SyntaxError(f"Invalid Assignment token character '{c}'"), char(string[index:]))

        else:
            assignment += c
            index += 1

    if len(assignment) == 0:
        lraise(SyntaxError(f"Assignment Token '{ASSIGNMENT_TOKEN}' has to be followed by at least 1 letter."),
               char(string[index:]))

    token_list.append((LT.ASSIGNMENT, assignment, char(string[index:])))
    return index
