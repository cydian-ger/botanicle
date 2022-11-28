from __future__ import annotations

from typing import Union
from dataclasses import dataclass
from datatypes import Name, Value_List, Expression
from lexer.static import ARG_OPEN, ARG_CLOSE


@dataclass(frozen=True, slots=True)
class LMatch:
    name: Name
    values: Value_List[Union[Name, Expression]]  # Variable names

    def __call__(self, *args) -> bool:
        if len(args) != self.var_len + 1:
            return False

        if args[0] != self.name:
            return False

        return True

    @property
    def var_len(self):
        return len(self.values)

    def __eq__(self, other: LMatch) -> bool:
        return (
                self.name == other.name and
                self.var_len == other.var_len
        )

    def __repr__(self):
        # no vars
        if len(self.values) == 0:
            return f"{self.name}"
        else:
            return f"{self.name}{ARG_OPEN}{', '.join([str(val) for val in self.values])}{ARG_CLOSE}"
