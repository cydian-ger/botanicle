from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from common.datatypes import Value_List, Name, Expression
from common.datatypes.LMatch import LMatch
from common.datatypes.LResult import LResult
from compiler.lexer.static import ASSIGNMENT_TOKEN, CONTEXT_LEFT, CONTEXT_RIGHT, CONDITION_TOKEN, RESULT_TOKEN, ARG_OPEN, \
    ARG_CLOSE


@dataclass
class Rule:
    # Names NEED to be unique
    match: LMatch  # A
    assignment: Optional[str]  # Name used by other rules to call it e.g. ".rule1" would be "'rule1'"
    left_context: Optional[Value_List[LMatch]]  # A(a) B(b) C(c) > SELF
    right_context: Optional[Value_List[LMatch]]  # SELF < A(a) B(b) C(c)
    condition: Optional[Value_List[Expression]]  # Condition :a == b =>
    result: Optional[Value_List[LResult]]

    def __post_init__(self):
        self.variables: Value_List[Name] = Value_List()
        self.variables.set_type(Name)

        if not self.match:
            return

        var_list = (self.left_context or []) + [self.match] + (self.right_context or [])

        for var in var_list:
            for var_name in var.values:
                if var_name in self.variables:
                    raise KeyError(f"Variable name '{var_name}' is defined more than once in the match.")
                else:
                    self.variables.append(var_name)

    def __eq__(self, other: Rule) -> bool:
        if not self.match and other.match:
            return False

        elif self.match != other.match:
            return False

        if self.left_context != other.left_context:
            return False

        if self.right_context != other.right_context:
            return False

        if self.condition != other.condition:
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

        if self.match:
            out_str += f"{self.match} "

        if self.right_context:
            if len(self.right_context) > 0:
                out_str += f"{CONTEXT_RIGHT} "
                out_str += " ".join([str(con) for con in self.right_context]) + " "

        if self.condition is not None:
            out_str += f"{CONDITION_TOKEN} "

            if len(self.condition) == 1:
                out_str += f"{self.condition[0]} "
            else:
                out_str += f"{ARG_OPEN}" \
                           f"{', '.join([str(con) for con in self.condition])}" \
                           f"{ARG_CLOSE} "

        out_str += f"{RESULT_TOKEN} "

        if self.result is not None:
            out_str += f"{' '.join([str(res) for res in self.result])}"

        return out_str
