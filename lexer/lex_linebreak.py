from lexer.LT import LT
from lexer.static import LINE_BREAK
from typing import List, Tuple, Any


def lex_linebreak(string: str, token_list: List[Tuple[LT, Any]] ) -> int:
    index = 0
    line_breaks: int = 0
    while index < len(string):
        char = string[index]
        if char != LINE_BREAK:
            break

        index += 1
        line_breaks += 1

    token_list.append((LT.NEW_LINE, line_breaks))
    return index
