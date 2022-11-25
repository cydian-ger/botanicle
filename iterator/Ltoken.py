from __future__ import annotations
from dataclasses import dataclass

# Actual used thing. A(1)
# Has to be associated to a rule
from datatypes import Name, Value_List


@dataclass(frozen=True, slots=True)
class LToken:
    name: Name
    values: Value_List[Name]

    @property
    def var_len(self):
        return len(self.values)

    def __eq__(self, other: LToken) -> bool:
        return (
                self.name == other.name and
                self.var_len == other.var_len
        )

    def __ne__(self, other: LToken) -> bool:
        return not self == other
