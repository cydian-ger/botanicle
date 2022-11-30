import ast
import sys
from typing import Optional, Dict, List
from collections import UserString

from compiler.lexer.static import ARGV_WARNING
from compiler.Lglobal import lraise, lwarn


class Expression(UserString):
    variables: List[str]

    def __init__(self, string: str, token_index, result_type: Optional[type] = None):
        super().__init__(string)

        root = None
        try:
            root = ast.parse(string)

            if not root.body:
                lraise(SyntaxError(f"Expression '{string}' is empty."), token_index)

        except SyntaxError:
            lraise(SyntaxError(f"String '{string}' is not a valid python expression."), token_index)

        variables: Dict[str, int] = {node.id: 1 for node in ast.walk(root) if isinstance(node, ast.Name)}

        self.variables = list(variables.keys())

        if sys.argv.__contains__(ARGV_WARNING):
            ugly_vars = [variable for variable in variables if variable.lower() != variable]
            if len(ugly_vars) > 0:
                lwarn(SyntaxWarning(f"Expression '{string}' contains variables with uppercase letters: "
                                    f"{', '.join(ugly_vars)}"))

        try:
            if result_type:
                try:
                    result = eval(string, None, variables)

                except ZeroDivisionError:  # Assume that if you divide by 0 the result would be 0
                    # Since the result of division is most likely a float.
                    result = 1.0

                if not isinstance(result, result_type):
                    lraise(TypeError(f"Expression '{string}' does not result in '{result_type.__name__}' type but "
                                     f"rather '{type(result).__name__}' type."), token_index)

        except SyntaxError as e:
            print(repr(e))
            lraise(SyntaxError(f"String '{string}' is not a valid expression as it does not result in a {result_type}.")
                   , token_index)
