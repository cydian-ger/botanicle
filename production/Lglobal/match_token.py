from compiler.lcompiler.bottle import Bottle
from production.static.lines import Line


def match_token(ltoken, bottle: Bottle):
    for rule in bottle.rule_list:
        Line.successor.append(rule.result)
    print(ltoken)
