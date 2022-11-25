from typing import Dict, Set, Optional
from datatypes import *


class Frame:
    # The frame contains all external information, like expose and include
    exposed_variable: Optional[Value_List[Token]]
    exposing_conditions: Optional[Value_List[int]]

    def __init__(self):
        self.exposed_variables = None
        self.exposing_conditions = None


class Bottle:
    variables: Dict[Name, Value]
    groups: Dict[Token, Value_List[Token]]
    context_ignore: Set[Token]
    frame: Frame

    def __init__(self):
        self.context_ignore = set()
        self.variables = dict()
        self.groups = dict()
        self.frame = Frame()

    def add_variable(self, variable_name: Name, variable_value: Value):
        if variable_name in self.variables:
            raise ValueError(f"Variable {variable_name} already defined.")

        self.variables[variable_name] = variable_value

    def __repr__(self):
        return f"variables: {self.variables}" \
               f"\ngroups: {self.groups}" \
               f"\ncontext_ignore: {self.context_ignore}"
