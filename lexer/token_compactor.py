from typing import List, Tuple, Any, Optional, Set

from lexer.LT import LT, LT_CLOSE
from lexer.static import TOKEN_PRIORITY


def token_compactor(token_list: List[Tuple[LT, Any]]) -> List[Tuple[LT, Any]]:
    out_list = list()
    _token_compactor(token_list, out_list)

    # Sort the list
    return sorted(out_list, key=lambda x: TOKEN_PRIORITY.get(x[0], len(TOKEN_PRIORITY) + 1))


def _token_compactor(token_list: List[Tuple[LT, Any]],
                     out_list: Optional[List[Tuple[LT, Any]]],
                     end_token: Optional[LT] = None) \
        -> int:

    index = 0
    while index < len(token_list):
        token, value = token_list[index]

        if token in LT_CLOSE.keys():
            index += 1
            sub_token_list = list()
            index += _token_compactor(token_list[index:], sub_token_list, LT_CLOSE[token])

            # All ending and opening blocks should have None
            if value is not None:
                raise NotImplementedError

            out_list.append((token, sub_token_list))

        elif token == end_token:
            break

        else:
            if token != LT.NEW_LINE:
                out_list.append((token, value))

        index += 1

    return index

