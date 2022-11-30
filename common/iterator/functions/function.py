from typing import List, Any, Dict
import common.iterator.functions.func_list as func_list
from compiler.lexer.static import FUNCTION_TOKEN


def func_type(): pass


def _get_type(func: type(func_type)) -> type:
    _type = func.__annotations__.get('return', None)

    # If its part of the typing Library
    if _type.__dict__.get('__origin__', False):
        _type = _type.__origin__

    return _type


def load_function(function_name: str, function_args: List[Any], expected_return_type: type):
    if function_name not in [func for func in dir(func_list) if not func.startswith("__")]:
        raise ModuleNotFoundError(f"There is no function named {FUNCTION_TOKEN}{function_name}")

    func = getattr(func_list, function_name)

    if _get_type(func) != expected_return_type:
        raise TypeError(f"Function {FUNCTION_TOKEN}{function_name} returns type '{_get_type(func).__name__}' "
                        f"but should return type '{expected_return_type.__name__}' instead.")

    # This seems to be always ordered
    types: Dict[Any, type] = func.__annotations__
    types.pop('return')
    types: List[type] = [v for k, v in types.items()]

    if len(types) != len(function_args):
        raise ValueError(f"Function {FUNCTION_TOKEN}{function_name} takes {len(types)} arguments but "
                         f"{len(function_args)} was provided")

    for index, _arg in enumerate(zip(function_args, types)):
        arg, arg_expected_type = _arg
        if type(arg) != arg_expected_type:
            raise TypeError(f"Function {FUNCTION_TOKEN}{function_name} expects '{arg_expected_type}' as {index + 1}."
                            f" argument but got {type(arg)} instead.")

    return func


if __name__ == '__main__':
    args = [1.0, 10.0, 1]
    print(load_function("seed", args, float)(*args))
    # Uppercase function refers to object e.g. $TTL_X = turtle_x coordinate
    # Lowercase function refers to function $seed = random seed
    # The function should be an object that can be returned when its loaded
    #
    # MATCH
    # Function in the match. $function(Argument) -> LMatch
    # Function in the match Arguments A($function) -> Not accepted because it should be
    #
    # CONDITION
    # Function instead of expression -> : ("a", $function("a")) -> bool value
    # Function inside of expression -> : ("a and $function("a")) -> NO IDEA YET
    #
    # RESULT
    # Function as result -> -> $function("a") -> LToken / LResult or something
    # Function as result argument -> A($function(1)) -> float
