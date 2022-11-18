from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.lex_error import LexError
from lexer.static import SPACE, LINE_BREAK, ARG_OPEN, FUNCTION_TOKEN, ARG_CLOSE, ARG_DELIMITER


def lex_function(string: str, token_list: List[Tuple[LT, Any]]) -> int:
    index = 0
    func = ""

    while index < len(string):
        c = string[index]

        if c == ARG_OPEN or c == SPACE or c == ARG_DELIMITER or c == ARG_CLOSE:
            token_list.append((LT.FUNCTION, func))
            # index -= 1
            break

        elif c == LINE_BREAK:
            raise LexError(f"Invalid Character LINE_BREAK in name", string[index:], SyntaxError)

        elif c == FUNCTION_TOKEN:
            if index != 0:
                raise LexError(f"Function token {FUNCTION_TOKEN} can not appear inside the function name",
                               string[index:], SyntaxError)

        else:
            func += c

        index += 1

    return index
