from types import LambdaType
from typing import Dict, List, Tuple, Any

from common.datatypes.expression_functions.proxy import Proxy
from common.iterator.functions.function import load_call


def load_object_calls(object_calls: List[Tuple[str, str, Any]], result_type, token_index) -> Dict[str, Proxy]:
    # Dictionary with the name of the object and the associated proxy
    objects: Dict[str, Proxy] = dict()
    for obj, attr, node in object_calls:
        # Get the parent object
        original_object = load_call(f"{obj}.{attr}", [], result_type,
                                    (token_index[0] + node.col_offset,
                                     token_index[0] + node.end_col_offset))

        # If the original object does not have a proxy yet, create one
        if obj not in objects:
            objects[obj] = Proxy(original_object)

        # Assign the object an attribute with the original attribute name
        # Wrap it in a lambda if it is not already
        object_attr = getattr(original_object, attr)
        if isinstance(object_attr, LambdaType):
            objects[obj].__setattr__(attr, object_attr)
        else:
            # Put getattr so it does not load it beforehand
            objects[obj].__setattr__(attr, lambda: getattr(original_object, attr))

    return objects
