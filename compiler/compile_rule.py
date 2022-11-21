from typing import List, Tuple, Any, Optional
from lexer.LT import LT


def compile_rule(token_list: List[Tuple[LT, Any]]):
    name: Optional[str] = None

    for token, content in token_list:
        if token not in {LT.ASSIGNMENT, LT.LTOKEN, LT.ARGS, LT.CONTEXT_TOKEN, LT.CONDITION, LT.RESULT,
                         LT.FUNCTION, LT.FUNCTION_ARGS}:
            raise SyntaxError

        if token in {LT.FUNCTION_ARGS, LT.ARGS}:
            pass
            # Check if the args are valid

    # F < F > F : con -> F
    # F < F : con -> F
    # F > F : con -> F
    # F : con -> F
    # F : -> F
    # F -> F
    # : con -> F
    # -> F
