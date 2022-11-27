import ast
import sys
from typing import Optional, Dict
from collections import UserString

from common.LWarning import LWarning
from lexer.static import ARGV_WARNING


class Expression(UserString):
    def __init__(self, string: str, result_type: Optional[type] = None):
        super().__init__(string)
        try:
            ast.parse(string)
        except SyntaxError:
            raise SyntaxError(f"String '{string}' is not a valid python expression.")

        root = ast.parse(string)
        variables: Dict[str, int] = {node.id: 1 for node in ast.walk(root) if isinstance(node, ast.Name)}

        if sys.argv.__contains__(ARGV_WARNING):
            ugly_vars = [variable for variable in variables if variable.lower() != variable]
            if len(ugly_vars) > 0:
                LWarning(f"Expression '{string}' contains variables with uppercase letters: {', '.join(ugly_vars)}",
                         SyntaxWarning).throw()

        try:
            if result_type:
                try:
                    result = eval(string, None, variables)

                except ZeroDivisionError:  # Assume that if you divide by 0 the result would be 0
                    result = 0.0

                if not isinstance(result, result_type):
                    raise TypeError(f"Expression '{string}' does not result in '{result_type.__name__}' type but "
                                    f"rather '{type(result).__name__}' type.")

        except SyntaxError:
            raise SyntaxError(f"String '{string}' is not a valid expression as it does not result in a bool.")
