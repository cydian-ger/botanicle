from typing import Dict, Set
from datatypes import *


class Bottle:
    variables: Dict[Name, Value]
    groups: Dict[Token, Value_List[Token]]
    context_ignore: Set[Token]

    def __init__(self):
        self.context_ignore = set()
        self.variables = dict()
        self.groups = dict()

    def add_variable(self, variable_name: Name, variable_value: Value):
        if variable_name in self.variables:
            raise ValueError(f"Variable {variable_name} already defined.")

        self.variables[variable_name] = variable_value

    def __repr__(self):
        return f"variables: {self.variables}" \
               f"\ngroups: {self.groups}" \
               f"\ncontext_ignore: {self.context_ignore}"
