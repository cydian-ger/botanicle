from dataclasses import dataclass
from typing import Optional

from common.datatypes import Value_List
from common.datatypes.LResult import LResult
from compiler.lexer.static import ASSIGNMENT_TOKEN, RESULT_TOKEN


@dataclass
class NamedResult:
    # The named results can be called by reference
    assignment: str
    result: Optional[Value_List[LResult]]

    def __repr__(self):
        out_str: str = ""

        if self.assignment:
            out_str += f"{ASSIGNMENT_TOKEN}{self.assignment} "

        out_str += f"{RESULT_TOKEN} "

        if self.result is not None:
            out_str += f"{' '.join([str(res) for res in self.result])}"

        return out_str
