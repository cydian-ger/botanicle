from lexer.LT import LT
from lexer.static import LINE_BREAK
from typing import List, Tuple, Any, Union
from lexer.lex_global import char


def lex_linebreak(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0
    line_breaks: int = 0
    while index < len(string):
        _char = string[index]
        if _char != LINE_BREAK:
            break

        index += 1
        line_breaks += 1

    token_list.append((LT.NEW_LINE, line_breaks, char(string[index:])))
    return index
