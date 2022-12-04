from typing import List, Any, Dict

from common.iterator.functions import func_list as func_list
from common.iterator.functions.func_util import _check_expected_type
from compiler.Lglobal import lraise
from compiler.lexer.static import FUNCTION_TOKEN


def _load_function(function_name: str, function_args: List[Any], expected_return_type: type, token_index):
    if function_name not in [func for func in dir(func_list) if not func.startswith("__")]:
        lraise(ModuleNotFoundError(f"There is no function named {FUNCTION_TOKEN}{function_name}"),
               token_index)

    func = getattr(func_list, function_name)

    _check_expected_type(expected_return_type, func, function_name, token_index)

    # This seems to be always ordered
    types: Dict[Any, type] = func.__annotations__
    types: List[type] = [v for k, v in types.items() if k != "return"]

    if len(types) != len(function_args):
        lraise(ValueError(f"Function {FUNCTION_TOKEN}{function_name} takes {len(types)} arguments but "
                          f"{len(function_args)} was provided"), token_index)

    for index, _arg in enumerate(zip(function_args, types)):
        arg, arg_expected_type = _arg
        if type(arg) != arg_expected_type:
            lraise(TypeError(f"Function {FUNCTION_TOKEN}{function_name} expects '{arg_expected_type}' as {index + 1}."
                             f" argument but got {type(arg)} instead."), token_index)

    return func
