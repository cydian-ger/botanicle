from typing import Tuple

from common.iterator.objects import LIterator
from common.iterator.rule import Rule
from compiler.lcompiler.bottle import Bottle
from production.static.lines import Line


def match_context(rule: Rule, bottle: Bottle, left) -> Tuple[bool, dict]:
    variables: dict = dict()

    if left:
        direction = -1
        context = reversed(rule.left_context)
    else:
        direction = 1
        context = rule.right_context

    # Load the current index
    con_iter = LIterator.index

    for con in context:
        con_iter += direction

        if con_iter < 0 or con_iter >= len(Line.predecessor):
            return False, {}
        # Load the token
        token = Line.predecessor[con_iter]

        #
        while token[0] in bottle.context_ignore:
            con_iter += direction

            if con_iter < 0 or con_iter > len(Line.predecessor):
                return False, {}

            token = Line.predecessor[con_iter]

        # Check if the context matches the token
        if not con.match(token):
            return False, {}

        # Load the variables into the variable map
        variables.update(**con.map(token[1:]))

    return True, variables
