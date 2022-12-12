from typing import Dict, Any, Union, get_origin, get_args

# This class just gets attributes added to it
from compiler.Lglobal import lraise


class Shell:
    pass


def evaluate_result(string: str, object_calls, result_type, variables, functions, token_index):

    try:
        # If the result type is a Union take the highest value
        if get_origin(result_type) == Union:
            result_type = get_args(result_type)[0]

        # Load testing variables
        test_vars: Dict[str, Any] = {v: result_type() for v in variables if v}

        # Load shell testing objects
        _objects: Dict[str, Shell] = dict()
        for obj, attr, _ in object_calls:
            if obj in _objects:
                _objects[obj].__setattr__(attr, result_type())
            else:
                shell = Shell()
                shell.__setattr__(attr, result_type())
                _objects[obj] = shell
        test_vars.update(**_objects)

        # Load testing functions
        _functions: Dict[str, Any] = dict()
        for func in functions:
            _functions[func] = lambda *x: result_type()

        test_vars.update(**_functions)

        # Check
        result = eval(string, None, test_vars)

    except ZeroDivisionError:  # Assume that if you divide by 0 the result would be 0
        # Since the result of division is most likely a float.
        result = 1.0

    if not isinstance(result, result_type):
        lraise(TypeError(f"Expression '{string}' does not result in '{result_type.__name__}' type but "
                         f"rather '{type(result).__name__}' type."), token_index)
