import ast
from typing import Dict, Any, List, Tuple

from common.iterator.functions.function import load_call
from compiler.Lglobal import lraise


def load_function_calls(function_calls: List[Tuple[Any, Any, Any]], result_type, token_index) \
        -> Dict[str, Any]:
    functions: Dict[str, Any] = dict()
    # Store the functions for later calls
    for function, function_args, node in function_calls:
        function_call_args = list()
        # Check all functions
        for function_arg in function_args:
            # If arg is a constant e.g. 1.0
            if type(function_arg) == ast.Constant:
                function_call_args.append(function_arg)
            # If arg is a variable
            elif type(function_arg) == ast.Name:
                function_call_args.append("1.0")  # Insert a place holder
            else:
                lraise(NotImplementedError(f"Function argument type: <{type(function_arg).__name__}> is not "
                                           f"implemented yet. Sowwy."), token_index)

        functions[function] = load_call(function, [ast.literal_eval(fa) for fa in function_call_args],
                                        result_type,
                                        (token_index[0] + node.col_offset,
                                         token_index[0] + node.end_col_offset))

    return functions
