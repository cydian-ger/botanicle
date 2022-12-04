from typing import get_origin, Union, get_args

from compiler.Lglobal import lraise
from compiler.lexer.static import FUNCTION_TOKEN


def func_type(): pass


def func_signature(name: str, func: type(func_type())) -> str:
    return f"${name}({', '.join([f'{k}: {v.__name__}' for k, v in func.__annotations__.items()])})"


def _get_type(func: type(func_type)) -> type:
    # Get the type of function
    _type = func.__annotations__.get('return', None)

    if _type is None:
        return type(None)

    # If its part of the typing Library
    if _type.__dict__.get('__origin__', False):
        _type = _type.__origin__

    return _type


def _check_expected_type(expected_return_type, func, function_name, token_index):
    # Check if the function return type is inside the expected return types
    if expected_return_type is not None:
        # If the args are packed in Union
        if get_origin(expected_return_type) == Union:
            # Checks the type against every type in loop
            type_match = [_get_type(func) == arg_type for arg_type in get_args(expected_return_type)]

            # If the function matches not a single type raise an Error
            if not (True in type_match):
                lraise(TypeError(f"Function {FUNCTION_TOKEN}{function_name} returns type "
                                 f"'{_get_type(func).__name__}' "
                                 f"but should return either type "
                                 f"'[{', '.join([str(arg.__name__) for arg in get_args(expected_return_type)])}]'"
                                 f" instead."), token_index)

        # If it is a single type hint
        elif _get_type(func) != expected_return_type:
            lraise(TypeError(f"Function {FUNCTION_TOKEN}{function_name} returns type '{_get_type(func).__name__}' "
                             f"but should return type '{expected_return_type.__name__}' instead."), token_index)