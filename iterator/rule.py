from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from datatypes import Value_List
from iterator.Ltoken import LToken
from lexer.static import ASSIGNMENT_TOKEN, CONTEXT_LEFT, CONTEXT_RIGHT, CONDITION_TOKEN, RESULT_TOKEN, ARG_OPEN, \
    ARG_CLOSE


@dataclass  # (frozen=True)
class Rule:
    # Names NEED to be unique
    match: LToken  # A
    assignment: Optional[str]  # Name used by other rules to call it e.g. ".rule1" would be "'rule1'"
    left_context: Optional[Value_List[LToken]]  # A(a) B(b) C(c) > SELF
    right_context: Optional[Value_List[LToken]]  # SELF < A(a) B(b) C(c)
    condition: Optional[str]  # Condition :a == b =>
    result: Optional[Value_List[LToken]]

    def __eq__(self, other: Rule) -> bool:

        if self.match != other.match:
            return False

        if self.left_context != other.left_context:
            return False

        if self.right_context != other.right_context:
            return False

        if self.condition != other.condition:
            return False

        if self.result != other.result:
            return False

        return True

    def __repr__(self):
        out_str: str = ""

        if self.assignment:
            out_str += f"{ASSIGNMENT_TOKEN}{self.assignment} "

        if self.left_context:
            if len(self.left_context) > 0:
                out_str += " ".join([str(con) for con in self.left_context])
                out_str += f" {CONTEXT_LEFT} "

        out_str += f"{self.match} "

        if self.right_context:
            if len(self.right_context) > 0:
                out_str += f"{CONTEXT_RIGHT} "
                out_str += " ".join([str(con) for con in self.right_context]) + " "

        out_str += f"{CONDITION_TOKEN} "
        if self.condition is not None:
            if len(self.condition) == 1:
                out_str += f"{self.condition[0]} "
            else:
                out_str += f"{ARG_OPEN}" \
                           f"{' '.join([str(con) for con in self.condition])}" \
                           f"{ARG_CLOSE} "

        out_str += f"{RESULT_TOKEN} "

        if self.result is not None:
            out_str += f"{' '.join([str(res) for res in self.result])}"

        return out_str
