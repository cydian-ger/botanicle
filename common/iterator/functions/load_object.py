from typing import List, Any

from common.iterator.functions import func_list as func_list
from common.iterator.functions.did_you_mean import closest_match
from common.iterator.functions.func_list import lobjects
from common.iterator.functions.func_util import validate_expected_type
from compiler.Lglobal import lraise
from compiler.lexer.static import FUNCTION_ATTRIBUTE_TOKEN


def _load_object(call_name: str, function_args: List[Any], expected_return_type: type, token_index):
    # If the naming scheme is not correct
    if call_name.count(FUNCTION_ATTRIBUTE_TOKEN) != 1:
        lraise(SyntaxError(f"Received object call with invalid Syntax. Correct syntax: 'OBJECT.Attribute'. "
                           f"Received '{call_name}' instead."), token_index)

    # Object Class name, Object Attribute name
    object_name, object_attribute = call_name.split(FUNCTION_ATTRIBUTE_TOKEN)

    # No arguments allowed
    if function_args:
        lraise(ValueError(f"Object {call_name} attribute does not take arguments"), token_index)

    # Check if the object exists
    _objects = lobjects()
    if object_name not in _objects:
        lraise(ModuleNotFoundError(f"There is no object named <{object_name}>. "
                                   f"{closest_match(object_name, _objects)} "), token_index)

    cls = getattr(func_list, object_name)

    # Check if the attribute exists within the object
    module_attr = [name for name, value in cls.__dict__.items() if not name.startswith("_")]
    if object_attribute not in module_attr:
        lraise(SyntaxError(f"Attribute <{object_attribute}> is not within selected class "
                           f"'{object_name}'.{closest_match(object_attribute, module_attr)}"
                           f" <{', '.join(module_attr)}>"), token_index)

    ret_type = cls.__annotations__[object_attribute]
    validate_expected_type(expected_return_type, ret_type, call_name, token_index)
    return cls
