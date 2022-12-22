from typing import List, Dict, Any, Tuple

from common.iterator.objects import LIterator
from common.iterator.rule import Rule
from compiler.lcompiler.bottle import Bottle
from production.static.lines import Line


def match_left_context(rule: Rule, bottle: Bottle) -> Tuple[bool, dict]:
    variables: dict = dict()

    con_iter = LIterator.index
    for left_context in reversed(rule.right_context):
        con_iter -= 1

        if con_iter < 0:
            return False, {}

        if LIterator in bottle.context_ignore:
            continue

        token = Line.predecessor[con_iter]

        if not left_context.match(token):
            return False, {}

        variables.update(**left_context.map(token[1:]))
    return True, variables


def match_token(ltoken: List, bottle: Bottle):
    for rule in bottle.rule_list:
        # check if it matches
        # then append the successor

        # This means the token is correct and has the right amount of values
        if not rule.match.match(ltoken):
            continue

        # Map the values from the token onto the variable name
        variables: Dict[str, Any] = {k: v for k, v in zip(rule.match.values, ltoken[1:])}

        if rule.right_context:
            pass

        if rule.left_context:
            res, _vars = match_left_context(rule, bottle)
            print(res, _vars)
            if not res:
                continue
            print(rule.left_context, LIterator.index, _vars)
            # check left context
            pass

        # Check all conditions and if at least 1 of them if False, check the next rule
        if rule.condition:
            failed = False
            for con in rule.condition:
                if con.evaluate(variables) is False:
                    failed = True
                    break
            if failed:
                continue

        for result in rule.result:
            if result.is_group():
                # TODO load the matched character if its a capture group
                raise NotImplementedError
            else:
                token = result.name

            Line.successor.append([token] + result.load(variables))
        return

    # What if no match is found
    Line.successor.append(ltoken)
