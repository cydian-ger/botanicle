from typing import List, Any

from common.iterator.functions.did_you_mean import closest_match
from common.iterator.functions.load_function import _load_function
from common.iterator.functions.load_object import _load_object
from compiler.Lglobal import lraise
from compiler.lexer.static import FUNCTION_ATTRIBUTE_TOKEN


def load_call(function_name: str, function_args: List[Any], expected_return_type: type, token_index):
    # Adjust for misalignment
    token_index = (token_index[0] + 2, token_index[1] + 2)

    if function_name[0].islower():
        # Check if the function has an attribute token
        if function_name.__contains__(FUNCTION_ATTRIBUTE_TOKEN):
            lraise(SyntaxError(f"A function can not have an attribute token '{FUNCTION_ATTRIBUTE_TOKEN}' in "
                               f"<{function_name}>. Either capitalize it to make it an object call or remove"
                               f"the attribute token."),
                   token_index)
        # Returns a function class
        return _load_function(function_name, function_args, expected_return_type, token_index)
    else:
        # Returns an object
        return _load_object(function_name, function_args, expected_return_type, token_index)


if __name__ == '__main__':
    pass
    # Uppercase function refers to object e.g. $TTL_X = turtle_x coordinate
    # Lowercase function refers to function $seed = random seed
    # The function should be an object that can be returned when its loaded
    # A function is always only called during production and can never turn into a token.
    #
    # MATCH
    # [ ] Function in the match. $function(Argument) -> LMatch
    # [ ] Function in the match Arguments A($function) -> Not accepted because an argument name does not change
    #       after compile so having a function there does not make sense
    #
    # CONDITION
    # [ ] Function instead of expression_functions -> : ("a", $function("a")) -> bool value
    # [x] Function inside of expression_functions -> : ("a and $function("a")) -> NO IDEA YET
    #
    # RESULT
    # [ ] Function as result -> -> $function("a") -> LToken / LResult or something
    # [ ] Function as result argument -> A($function(1)) -> floats
    # [x] Function inside of result expression_functions A("$seed() + 1")
    #
    # MAYBE have statement functions like:
    # define z as "1 + (0.1 * $IT.i())"
    # This starts at 0.1 but grows by 0.2 every new iteration.
    # sth like that.
