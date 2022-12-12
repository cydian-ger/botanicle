from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.static import SPACE, LINE_BREAK, ARG_OPEN, FUNCTION_TOKEN, ARG_CLOSE, ARG_DELIMITER, \
    FUNCTION_EXTRA_TOKEN
from compiler.Lglobal import char, lraise


def lex_function(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0
    func = ""

    while index < len(string):
        c = string[index]

        if c == ARG_OPEN or c == SPACE or c == ARG_DELIMITER or c == ARG_CLOSE:
            if func == "":
                lraise(SyntaxError(f"Function name must not be empty"), char(string[index:]))
            token_list.append((LT.FUNCTION, func, char(string[index:])))
            # index -= 1
            break

        elif c == LINE_BREAK:
            lraise(SyntaxError(f"A Function can not be followed a LINE_BREAK"), char(string[index:]))

        elif c == FUNCTION_TOKEN:
            if index != 0:
                lraise(SyntaxError(f"Function token '{FUNCTION_TOKEN}' can not appear inside the function name"),
                       char(string[index:]))

        else:
            if not c.isalnum() and c not in FUNCTION_EXTRA_TOKEN:
                lraise(SyntaxError(f"The Character '{c}' is not allowed in a function name."), char(string[index:]))
            func += c

        index += 1

    return index
