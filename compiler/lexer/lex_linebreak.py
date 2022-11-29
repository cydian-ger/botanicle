from compiler.lexer.LT import LT
from compiler.lexer.static import LINE_BREAK
from typing import List, Tuple, Any, Union
from compiler.lexer.lex_global import char


def lex_linebreak(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0
    line_breaks: int = 0
    while index < len(string):
        _char = string[index]
        if _char != LINE_BREAK:
            break

        index += 1
        line_breaks += 1

    # Minus one because line break is the end for rule and statement
    token_list.append((LT.NEW_LINE, line_breaks, char(string[index - 1:])))
    return index
