from typing import List, Tuple, Any, Optional, Union

from compiler.lexer.LT import LT, LT_CLOSE
from compiler.lexer.static import TOKEN_PRIORITY


def token_compactor(token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]) -> \
        List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]:
    out_list = list()
    _token_compactor(token_list, out_list)

    # Sort the list
    return sorted(out_list, key=lambda x: TOKEN_PRIORITY.get(x[0], len(TOKEN_PRIORITY) + 1))


def _token_compactor(token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]],
                     out_list: Optional[List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]],
                     end_token: Optional[LT] = None) \
        -> Tuple[int, int]:

    char_index = 0
    index = 0
    while index < len(token_list):
        token, value, char_index = token_list[index]

        if token in LT_CLOSE.keys():
            index += 1
            sub_token_list = list()
            _add_i, char_index_end = _token_compactor(token_list[index:], sub_token_list, LT_CLOSE[token])
            index += _add_i

            # All ending and opening blocks should have None
            if value is not None:
                raise NotImplementedError

            out_list.append((token, sub_token_list, (char_index, char_index_end)))

        elif token == end_token:
            break

        else:
            if token != LT.NEW_LINE:
                if isinstance(value, dict):
                    out_list.append((token, value, (char_index + 1, char_index + 1)))
                else:
                    value: str
                    length = len(value)
                    # Add 1 length for the removed character
                    if token in {LT.ASSIGNMENT, LT.FUNCTION, LT.REFERENCE}:
                        length += 1

                    # If a token is known to have a defined length and its already saved -> "_"
                    if isinstance(char_index, tuple):
                        out_list.append((token, value, char_index))
                    else:
                        out_list.append((token, value, (char_index - length, char_index)))

        index += 1

    return index, char_index

