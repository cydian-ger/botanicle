from __future__ import annotations
from dataclasses import dataclass

# Actual used thing. A(1)
# Has to be associated to a rule
from datatypes import Name, Value_List
from lexer.static import ARG_OPEN, ARG_CLOSE


@dataclass(frozen=True, slots=True)
class LMatch:
    name: Name
    values: Value_List[Name]  # Variable names

    @property
    def var_len(self):
        return len(self.values)

    def __eq__(self, other: LMatch) -> bool:
        return (
                self.name == other.name and
                self.var_len == other.var_len
        )

    def __ne__(self, other: LMatch) -> bool:
        return not self == other

    def __repr__(self):
        # no vars
        if len(self.values) == 0:
            return f"{self.name}"
        else:
            return f"{self.name}{ARG_OPEN}{', '.join([str(val) for val in self.values])}{ARG_CLOSE}"
