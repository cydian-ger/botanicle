from typing import List, Any

from common.iterator.functions import func_list as func_list
from compiler.Lglobal import lraise
from compiler.lexer.static import FUNCTION_EXTRA_TOKEN, FUNCTION_TOKEN


def _load_object(call_name: str, function_args: List[Any], expected_return_type: type, token_index):
    # If the naming scheme is not correct
    if call_name.count(FUNCTION_EXTRA_TOKEN) != 1:
        lraise(SyntaxError(f"Received object call with invalid Syntax. Correct syntax: 'OBJECT.Attribute'. "
                           f"Received '{call_name}' instead."), token_index)

    object_name, object_attribute = call_name.split(FUNCTION_EXTRA_TOKEN)

    # No arguments allowed
    if function_args:
        lraise(ValueError(f"Object {call_name} attribute does not take arguments"), token_index)

    # Check if the object exists
    if object_name not in [obj for obj in dir(func_list) if not obj.startswith("__")]:
        lraise(ModuleNotFoundError(f"There is no object named {FUNCTION_TOKEN}{call_name}"), token_index)

    cls = getattr(func_list, object_name)

    # Check if the attribute exists within the object
    module_attr = [name for name, value in cls.__dict__.items() if not name.startswith("__")]
    if object_attribute not in module_attr:
        lraise(SyntaxError(f"Searched Attribute '{object_attribute}' is not within selected class "
                           f"'{object_name}'. <{', '.join(module_attr)}>"), token_index)

    ret_type = cls.__annotations__[object_attribute]

    if ret_type != expected_return_type:
        lraise(TypeError(f"Function {FUNCTION_TOKEN}{call_name} returns type '{ret_type.__name__}' "
                         f"but should return type '{expected_return_type.__name__}' instead."), token_index)

    return cls
