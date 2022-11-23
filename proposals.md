# P.C.M.S.
Parametric  A(a)
Context Sensitive A < B > C
Modular leaf.l
Stochastic %


# New Proposal float-standardization:
Every value, with a value being what is inside the actual numbers inside L-Token during production,
these values can only be a float.

# New Proposal '$' / functions:
$ this is now the function keyword.
At any point where an L-token can be there can also be a function
Define concrete behaviour.
Whenever $ is called it is replaced by a function call
What a function returns is dictated by the context it appears in.
E.g. in A < $func > B $func must be an LToken
while in ($func, $func2) $func and $func2 must be an argument
while in ("$func ") $func must be an expression
an argument inside of a $func (-> $func($func)) can be anything

function idea list:
$weighted(weight1: @linename1, ... weightN: @linename2): -> LToken

$seed (min: int, max: int) : -> value, takes the seed (that is between 0 and 1) and normalizes it to be between
 those two numbers.

$prev_LT / $next_LT (*arg_names): -> LToken. 
$prev_LT(*arg_names): -> LToken: this can only be used inside of context or result.
It takes the current cursor position and the symbol associated and matches and takes the shape of the previous match
$next_LT(*arg_names): -> LToken: does the same but for the right side of the string. e.g.
start: 0AB0BA0
rule $prev_LT < 0 > $next_LT :-> 1
only the 0 at index 3 would turn into a 1 

$m_group((...): List of LToken, (...): List of arguments)
e.g. $m_group((A, B, C),(x1, x2)) would match any A B or C with 2 arguments

# Proposal 'Line alias':
you can alias lines to reference them
with the reference syntax beginning with a period followed by any string
e.g.
ω1: A < B > C:→ ABC

or in a practical case
.a1 A < B > C:→ (10: a_1, 40: a_2, 50: a_3)
.a_1 →A
.a_2 →A
.a_3 →A

Alternatively it could also be denoted with a dot at the start
.line1 A < B > C:→ .line2

In post these rules will be merged (e.g. implement partial rule)

What if for weighted results there are 2 types:

# New Proposal 2
Extend the expose keyword with the with keyword allowing condition expressions
expose (x, y, z) as (a, b, c) with ("a > b > c", "b > 0")