from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
from iterator.Ltoken import LToken
from iterator.context import Context
import sys


@dataclass  # (frozen=True)
class Rule:
    # Names NEED to be unique
    name: str  # A
    assignment: Optional[str]  # Name used by other rules to call it e.g. ".rule1" would be "'rule1'"
    variables: List[str]  # A, A(), A(a, b), A(a, b, c)
    left_context: Optional[List[Context]]  # A(a) B(b) C(c) > SELF
    right_context: Optional[List[Context]]  # SELF < A(a) B(b) C(c)
    condition: Optional[str]  # Condition :a == b =>

    # result: Optional[List[LSystem]]  # => A(a)
    # List of Result + eval

    def fits(self, token: LToken) -> bool:
        # Checks if the token is eligible to be checked for context and condition
        return (
            self.name == token.name and
            len(self.variables) == token.var_len
        )

    def context(self, left: Optional[List[LToken]], right: Optional[List[LToken]]) -> bool:
        # Loop and check if all contexts match
        for index, context_left in enumerate(left):
            if context_left != self.left_context[index]:
                return False

        for index, context_right in enumerate(right):
            if context_right != self.right_context[index]:
                return False

        return True

    def condition(self) -> bool:
        # Add values and context
        if self.condition is None:
            return True

        # LOGIC IN HERE
        return True

    def ecc(self, token: LToken, context_left: Optional[List[LToken]], context_right: Optional[List[LToken]]) -> bool:
        # ECC
        # Eligibility
        # Contex
        # Condition
        # CALL THE THINGS
        return True

    def __hash__(self):
        # Only if the name, the amount of variables and the condition are not
        return hash((self.name, len(self.variables), self.condition))


if __name__ == '__main__':
    # Have a flag for checking of all expressions are correct
    sys.argv.append("")
    # A(a, b)
    # C(c) < A(a) > B(b)     : a == b    ⇒ A(a + 1) Z(1)
    rule = Rule(
        name="L",
        variables=list(),
        left_context=None,
        right_context=None,
        condition=None
    )
    print(rule)
