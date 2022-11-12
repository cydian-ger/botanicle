from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.lex_linebreak import lex_linebreak
from lexer.static import LINE_BREAK


def lex_comment(string: str, token_list: List[Tuple[LT, Any]]) -> int:
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

    token_list.append((LT.COMMENT, comment))
    return index
