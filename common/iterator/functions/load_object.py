from typing import List, Any

from common.iterator.functions import func_list as func_list
from common.iterator.functions.func_util import _check_expected_type
from compiler.Lglobal import lraise
from compiler.lexer.static import FUNCTION_EXTRA_TOKEN, FUNCTION_TOKEN


def _load_object(call_name: str, function_args: List[Any], expected_return_type: type, token_index):
    # If the naming scheme is not correct
    if call_name.count(FUNCTION_EXTRA_TOKEN) != 1:
        raise SyntaxError()

    object_name, object_attribute = call_name.split(FUNCTION_EXTRA_TOKEN)

    # No arguments allowed
    # TODO: check for function args.

    # Check if the object exists
    if object_name not in [obj for obj in dir(func_list) if not obj.startswith("__")]:
        lraise(ModuleNotFoundError(f"There is no function named {FUNCTION_TOKEN}{call_name}"), token_index)

    cls = getattr(func_list, object_name)

    # Check if the attribute exists within the object
    module_attr = [name for name, value in cls.__dict__.items() if not name.startswith("__")]
    if object_attribute not in module_attr:
        lraise(SyntaxError(f"Searched Attribute '{object_attribute}' is not within selected class "
                           f"'{object_name}'. <{', '.join(module_attr)}>"), token_index)

    func = getattr(cls, object_attribute)

    _check_expected_type(expected_return_type, func, call_name, token_index)

    return func
