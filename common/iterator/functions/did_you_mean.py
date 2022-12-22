from typing import List

from common.env import env_args
from compiler.lexer.static import ARGV_DEBUG


def closest_match(in_word: str, compare_list: List[str]):
    _match_list = list()
    for compare_word in compare_list:
        # Add the distance
        length_difference = abs(len(in_word) - len(compare_word))

        character_difference = 0
        correct_characters = 0
        for base_char, compare_char in zip(in_word, compare_word):
            if base_char != compare_char:
                character_difference += 1
            else:
                correct_characters += 1

        _match_list.append(
            (compare_word,
             character_difference / min(len(in_word), len(compare_word)),
             length_difference,
             correct_characters)
        )

    # x[3] minus cause the total amount counts
    _match_list.sort(key=lambda x: (x[1], x[2], -x[3]))
    _match = _match_list[0]

    if env_args.__contains__(ARGV_DEBUG):
        # closest_name = f"{closest_name} (diff: {_match[0]})"
        pass

    if _match[1] > 0.5:
        return ""

    return f" Did you mean <{_match[0]}>?"
