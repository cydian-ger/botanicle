from __future__ import annotations
from typing import Union, Dict, Any
# from dataclasses import dataclass
from common.datatypes import Expression, Value_List, Token
from common.datatypes.lgroup import Group
from compiler.lexer.static import ARG_OPEN, ARG_CLOSE, EXPR


def _wrap(string):
    return EXPR + str(string) + EXPR


class LResult:
    name: Token
    values: Value_List[Expression]
    _is_group: bool

    def __init__(self, name: Token, values: Value_List[Expression], is_group: bool):
        self.name = name
        self.values = values
        self._is_group = is_group

    def is_group(self):
        return self._is_group

    def __repr__(self):
        # no vars
        if len(self.values) == 0:
            return f"{self.name}"
        else:
            return f"{self.name}{ARG_OPEN}{', '.join([_wrap(val) for val in self.values])}{ARG_CLOSE}"

    def load(self, eval_vars: Dict[str, Any]):
        return [res.evaluate(eval_vars) for res in self.values]
