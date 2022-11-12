from __future__ import annotations
from dataclasses import dataclass
from typing import List


# Actual used thing. A(1)
# Has to be associated to a rule
@dataclass(frozen=True, slots=True)
class Context:
    name: str
    values: List[str]

    @property
    def var_len(self):
        return len(self.values)

    def __eq__(self, other) -> bool:
        return (
                self.name == other.name and
                self.var_len == other.var_len
        )

    def __ne__(self, other) -> bool:
        return not self == other
