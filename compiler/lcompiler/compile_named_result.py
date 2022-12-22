from typing import Optional

from common.datatypes import Value_List, Expression
from common.datatypes.LMatch import LMatch
from common.iterator.named_result import NamedResult
from compiler.Lglobal import lraise
from compiler.lcompiler.bottle import Bottle
from compiler.lexer.static import START_RULE, VALID_START_TOKENS


def compile_named_result(name: Optional[str], result: Optional[Value_List[LMatch]], bottle: Bottle, line_token):
    named_result = NamedResult(
        assignment=name,
        result=result
    )

    for result_token in result:
        if result_token.name.data not in VALID_START_TOKENS and \
                result_token.name.data not in bottle.frame.linked_files.keys():
            lraise(SyntaxError(f"Start contains an invalid token '{result_token.name}'. "
                               f"Start can only contain: '{VALID_START_TOKENS}' as well as "
                               f"{list(bottle.frame.linked_files.keys())} (included files)"), line_token[2])

    if name == START_RULE:
        if result is None or len(result) == 0:
            lraise(ValueError(f"Starting Axiom mustn't be empty. Received: {result}"), line_token[2])
        bottle.start = named_result  # Put the result here
    else:
        bottle.named_results.append(named_result)
