from typing import List, Tuple, Any
from lexer.LT import LT


# This compiles a single file
def l_compile(token_list: List[Tuple[LT, Any]]):
    for token, content in token_list:
        content: List[Tuple[LT, Any]]

        match token:
            case LT.STATEMENT:
                pass

            case LT.RULE:
                pass

            case LT.COMMENT:
                # Comments are skipped for now
                continue

    pass

