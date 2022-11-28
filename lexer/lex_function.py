from typing import List, Tuple, Any, Union
from lexer.LT import LT
from lexer.lex_error import LexError
from lexer.static import SPACE, LINE_BREAK, ARG_OPEN, FUNCTION_TOKEN, ARG_CLOSE, ARG_DELIMITER
from lexer.lex_global import char


def lex_function(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0
    func = ""

    while index < len(string):
        c = string[index]

        if c == ARG_OPEN or c == SPACE or c == ARG_DELIMITER or c == ARG_CLOSE:
            if func == "":
                raise LexError(f"Function name must not be empty", string[index:], SyntaxError)
            token_list.append((LT.FUNCTION, func, char(string[index:])))
            # index -= 1
            break

        elif c == LINE_BREAK:
            raise LexError(f"Invalid Character LINE_BREAK in name", string[index:], SyntaxError)

        elif c == FUNCTION_TOKEN:
            if index != 0:
                raise LexError(f"Function token '{FUNCTION_TOKEN}' can not appear inside the function name",
                               string[index:], SyntaxError)

        else:
            if not c.isalnum():
                raise LexError(f"The Character '{c}' is not allowed in a function name.", string[index:], SyntaxError)
            func += c

        index += 1

    return index
