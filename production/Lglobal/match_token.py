from typing import List, Dict, Any

from compiler.lcompiler.bottle import Bottle
from production.Lglobal.match_context import match_context
from production.static.lines import Line


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
            res, _vars = match_context(rule, bottle, False)
            if not res:
                continue
            variables.update(**_vars)

        if rule.left_context:
            res, _vars = match_context(rule, bottle, True)
            if not res:
                continue
            variables.update(**_vars)

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
                # The fetched result must be the one that matched
                token = ltoken[0]
            else:
                token = result.name.data

            Line.successor.append([token] + result.load(variables))
        return

    # What if no match is found
    Line.successor.append(ltoken)
