from __future__ import annotations
from typing import Union, Tuple, List
# from dataclasses import dataclass
from common.datatypes import Name, Value_List, Token
from common.datatypes.lgroup import Group
from compiler.lexer.static import ARG_OPEN, ARG_CLOSE, GENERIC


class LMatch:
    name: Union[Token, Group]
    values: Value_List[Name]
    _is_group: bool = False

    def __init__(self, name: Union[Token, Group], values: Value_List[Name]):
        self.name = name
        self.values = values

        if type(self.name) == Group:
            self._is_group = True

    @property
    def var_len(self):
        return len(self.values)

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.values != other.values:
            return False
        return True

    def match(self, instance: List):
        if self._is_group:
            if self.name.name != GENERIC:
                if instance[0] not in self.name:
                    return False

        else:
            if instance[0] != self.name:
                return False

        if len(instance) - 1 != self.var_len:
            return False

        return True

    def map(self, variables: List[float]):
        # Map the string data of the names onto the given values
        # This method assumes the length of the variables is equal to that of the values
        return {k.data: v for k, v in zip(self.values, variables)}

    def __repr__(self):
        # no vars
        if self.var_len == 0:
            return f"{self.name}"
        else:
            return f"{self.name}{ARG_OPEN}{', '.join([str(val) for val in self.values])}{ARG_CLOSE}"
