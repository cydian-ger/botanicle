import ast
from typing import Optional
from collections import UserString


class Expression(UserString):
    def __init__(self, string: str, result_type: Optional[type] = None):
        super().__init__(string)
        try:
            ast.parse(string)
        except SyntaxError:
            raise SyntaxError(f"String '{string}' is not a valid python expression.")

        root = ast.parse(string)
        variables = {node.id: 1 for node in ast.walk(root) if isinstance(node, ast.Name)}

        try:
            if result_type:
                result = eval(string, None, variables)

                if not isinstance(result, result_type):
                    raise TypeError(f"Expression '{string}' does not result in '{result_type.__name__}' type but "
                                    f"rather '{type(result).__name__}' type.")

        except SyntaxError:
            raise SyntaxError(f"String '{string}' is not a valid expression as it does not result in a bool.")
