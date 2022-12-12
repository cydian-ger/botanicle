import ast
from typing import Optional, Dict, List, Any
from collections import UserString

from common.datatypes.expression_functions.evalute_result import evaluate_result
from common.datatypes.expression_functions.load_function_calls import load_function_calls
from common.datatypes.expression_functions.load_object_calls import load_object_calls
from common.datatypes.expression_functions.proxy import Proxy
from common.env import env_args
from compiler.lexer.static import ARGV_WARNING, EXPR
from compiler.Lglobal import lraise, lwarn


class Expression(UserString):
    variables: List[str]
    functions: Dict[str, Any]
    objects: Dict[str, Any]

    def evaluate(self, eval_vars: Dict[str, Any]):
        return eval(self.data, None, {**eval_vars, **self.functions, **self.objects})

    def __init__(self, string: str, token_index, result_type: Optional[type] = None):
        try:
            # This checks if an expression_functions is valid
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
            self.functions: Dict[str, Any] = load_function_calls(
                function_calls,
                result_type,
                token_index
            )

            # Load all the object attribute calls and check if they are valid
            self.objects: Dict[str, Proxy] = load_object_calls(
                object_calls,
                result_type,
                token_index
            )

            if env_args.__contains__(ARGV_WARNING):
                ugly_vars = [variable for variable in variables if variable.lower() != variable]
                if len(ugly_vars) > 0:
                    lwarn(SyntaxWarning(f"Expression '{string}' contains variables with uppercase letters: "
                                        f"{', '.join(ugly_vars)}"))

            if result_type:
                evaluate_result(
                    string=string,
                    object_calls=object_calls,
                    result_type=result_type,
                    variables=self.variables,
                    functions=self.functions,
                    token_index=token_index
                )


        except SyntaxError as e:
            lraise(SyntaxError(f"String '{string}' is not a valid expression as it does not result in a {result_type}.")
                   , token_index)

        except Exception as e:
            raise e
            lraise(Exception(f"Failed due too uncaught exception: {repr(e)}"), token_index)
