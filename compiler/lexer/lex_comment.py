from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.lex_linebreak import lex_linebreak
from compiler.lexer.static import LINE_BREAK
from compiler.compiler_global import char


def lex_comment(string: str, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> int:
    index = 0
    comment = ""
    for c in string:
        if c == LINE_BREAK:
            index += lex_linebreak(string[index:], token_list)
            break

        # Exclude hashtag from comment
        if index != 0:
            comment += c

        index += 1

    token_list.append((LT.COMMENT, comment, char(string[index:])))
    return index
