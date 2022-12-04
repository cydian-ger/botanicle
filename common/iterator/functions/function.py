from typing import List, Any
from common.iterator.functions.load_function import _load_function
from common.iterator.functions.load_object import _load_object


def load_call(function_name: str, function_args: List[Any], expected_return_type: type, token_index):
    if function_name[0].islower():
        return _load_function(function_name, function_args, expected_return_type, token_index)
    else:
        return _load_object(function_name, function_args, expected_return_type, token_index)


if __name__ == '__main__':
    from compiler.Lglobal import init_compiler

    init_compiler("test")

    print(load_call("test", [1.0], float, 0))

    args = [1.0, 10.0, 1]
    print(load_call("seed", args, float, 0)(*args))

    # Uppercase function refers to object e.g. $TTL_X = turtle_x coordinate
    # Lowercase function refers to function $seed = random seed
    # The function should be an object that can be returned when its loaded
    # A function is always only called during production and can never turn into a token.
    #
    # MATCH
    # Function in the match. $function(Argument) -> LMatch
    # Function in the match Arguments A($function) -> Not accepted because an argument name does not change
    #       after compile so having a function there does not make sense
    #
    # CONDITION
    # Function instead of expression -> : ("a", $function("a")) -> bool value
    # Function inside of expression -> : ("a and $function("a")) -> NO IDEA YET
    #
    # RESULT
    # Function as result -> -> $function("a") -> LToken / LResult or something
    # Function as result argument -> A($function(1)) -> floats
    # Function inside of result expression A("$seed() + 1")
    #
    # MAYBE have statement functions like:
    # define z as "1 + (0.1 * $IT.i())"
    # This starts at 0.1 but grows by 0.2 every new iteration.
    # sth like that.
