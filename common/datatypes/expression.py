import ast
import sys
from typing import Optional, Dict, List, Any, Tuple
from collections import UserString

from common.iterator.functions.function import load_call
from compiler.lexer.static import ARGV_WARNING, EXPR
from compiler.Lglobal import lraise, lwarn


# This class just gets attributes added to it
class Shell:
    pass


class Expression(UserString):
    variables: List[str]
    functions: Dict[str, Any]
    objects: Dict[Tuple[str, str], Any]

    def __init__(self, string: str, token_index, result_type: Optional[type] = None):
        try:
            # This checks if an expression is valid
            super().__init__(string)

            # Remove '"' if necessary
            string = string.strip(EXPR)

            root = None
            try:
                root = ast.parse(string)

                if not root.body:
                    lraise(SyntaxError(f"Expression '{string}' is empty."), token_index)

            except SyntaxError:
                lraise(SyntaxError(f"String '{string}' is not a valid python expression."), token_index)

            # Get all variable assignment names
            var_list = [node.id for node in ast.walk(root) if isinstance(node, ast.Name)]

            # Function names and object calls
            try:
                function_calls = [(node.func.id, node.args, node) for
                                  node in ast.walk(root) if isinstance(node, ast.Call)]

                object_calls = [(node.value.id, node.attr, node)
                                for node in ast.walk(root) if isinstance(node, ast.Attribute)]

            except Exception as e:
                lraise(SyntaxError(f"Uncaught error during Expression: {str(e)}"), token_index)
                return

            # Load all functions
            function_names = [name for name, args, node in function_calls]
            # Load all Objects
            object_names = [name for name, attr, node in object_calls]

            # TODO
            # Check if variable is defined twice

            # Load a dummy value into every variable and leave out every function call and object
            variables: Dict[str, int] = {v: 1 for v in var_list if not (v in function_names or v in object_names)}

            # Load all the variable names
            self.variables = list(variables.keys())

            # Load all the functions to see if they are valid
            self.functions = dict()
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

                self.functions[function] = load_call(function, [ast.literal_eval(fa) for fa in function_call_args],
                                                     result_type,
                                                     (token_index[0] + node.col_offset,
                                                      token_index[0] + node.end_col_offset))

            # Load all the object attribute calls and check if they are valid
            self.objects = dict()
            for obj, attr, node in object_calls:
                self.objects[(obj, attr)] = load_call(f"{obj}.{attr}", [], result_type,
                                                      (token_index[0] + node.col_offset,
                                                       token_index[0] + node.end_col_offset))

            # Style guide
            if sys.argv.__contains__(ARGV_WARNING):
                ugly_vars = [variable for variable in variables if variable.lower() != variable]
                if len(ugly_vars) > 0:
                    lwarn(SyntaxWarning(f"Expression '{string}' contains variables with uppercase letters: "
                                        f"{', '.join(ugly_vars)}"))

            try:
                if result_type:
                    try:
                        # Load test variables
                        test_vars: Dict[str, Any] = {v: 1 for v in self.variables if v}

                        # Load shell test objects
                        _objects: Dict[str, Shell] = dict()
                        for obj, attr in self.objects.keys():
                            if obj in _objects:
                                _objects[obj].__setattr__(attr, 1)
                            else:
                                shell = Shell()
                                shell.__setattr__(attr, 1)
                                _objects[obj] = shell
                        test_vars.update(**_objects)

                        # Load test functions
                        _functions: Dict[str, Any] = dict()
                        for func in self.functions:
                            _functions[func] = lambda *x: 1

                        test_vars.update(**_functions)

                        # Check
                        result = eval(string, None, test_vars)

                    except ZeroDivisionError:  # Assume that if you divide by 0 the result would be 0
                        # Since the result of division is most likely a float.
                        result = 1.0

                    if not isinstance(result, result_type):
                        lraise(TypeError(f"Expression '{string}' does not result in '{result_type.__name__}' type but "
                                         f"rather '{type(result).__name__}' type."), token_index)

            except SyntaxError as e:
                lraise(SyntaxError(f"String '{string}' is not a valid expression as it does not result in a {result_type}.")
                       , token_index)

        except Exception as e:
            lraise(Exception(f"Failed due too uncaught exception: {repr(e)}"), token_index)
