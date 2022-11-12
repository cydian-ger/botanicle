from iterator.Ltoken import LToken
from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass(frozen=True)
class LFactory:
    tokens: List[str]
    expressions: Optional[List[List[str]]]

    def generate(self, variables: Dict[str, int]) -> List[LToken]:
        token_list: List[LToken] = list()

        if self.tokens is []:
            return list()

        for token, expressions in zip(self.tokens, self.expressions):
            # Populate the token with the correct values
            values: List[int] = [eval(expr, None, variables) for expr in expressions]

            token_list.append(LToken(
                name=token,
                values=values
            ))
