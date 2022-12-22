from typing import List, Optional

from common.datatypes import Value_List, Expression
from common.datatypes.LMatch import LMatch
from common.iterator.rule import Rule
from compiler.Lglobal import lraise
from compiler.lcompiler.bottle import Bottle
from compiler.lexer.static import START_RULE


def compile_full_rule(match_list: List[LMatch], name: Optional[str],
                      left_context: Optional[List[LMatch]], right_context: Optional[List[LMatch]],
                      condition: Optional[Value_List[Expression]], result: Optional[Value_List[LMatch]],
                      bottle: Bottle, line_token):

    _match = match_list[0]
    # Create the rule
    rule = Rule(
        match=_match,
        assignment=name,
        left_context=left_context,
        right_context=right_context,
        condition=condition,
        result=result
    )

    if rule in bottle.rule_list:
        lraise(SyntaxError(f"There already exists a rule with equivalent match for the rule: '{rule}'"), line_token[2])

    for variable in rule.variables:
        if variable in bottle.variables.keys():
            lraise(KeyError(f"Match Variable '{variable}' overrides defined variable."), line_token[2])

    if name == START_RULE:
        lraise(TypeError(f"Start Rule has to be a named result and not a rule"), line_token[2])

    bottle.rule_list.append(rule)
