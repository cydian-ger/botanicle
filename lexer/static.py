from lexer.LT import LT

LINE_BREAK: str = "\n"
EXPR = '"'
ARG_OPEN = "("
ARG_CLOSE = ")"
ARG_DELIMITER = ","  # For A(1, b)
SPACE = " "

# > (e.g. c_ignore)
CONTEXT_TOKENS = "<>"
CONDITION_TOKEN = ":"
RESULT_TOKEN = "→"
ASSIGNMENT_TOKEN = "."  # Assign a name to a rule
FUNCTION_TOKEN = "$"

BASE_AXIOMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CONTEXT_HINTS = "01234567889"
SPECIAL_AXIOMS = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"  # All of these are greek letters
# Limitation: these can only be used when
# a) referencing an include file
# b) for a catch group (that one only has rule wide scope)

__ = "αβγδεζηθικλμνξοπρσςτυφχψω"  # These are used for naming rules and lines and such

PRODUCTION_RULES = "[]{}+-"
GENERIC = "*"

# All tokens that can be used in rules A, *, [, ]
VALID_RULE_LTOKENS = BASE_AXIOMS + PRODUCTION_RULES + GENERIC + SPECIAL_AXIOMS + CONTEXT_HINTS

# Valid characters that denote the start of a rule
VALID_RULE_START = VALID_RULE_LTOKENS + RESULT_TOKEN + CONDITION_TOKEN + ASSIGNMENT_TOKEN + FUNCTION_TOKEN

# All tokens that can be used everywhere
VALID_INSTANCE_LTOKENS = BASE_AXIOMS + PRODUCTION_RULES + SPECIAL_AXIOMS

VALID_STATEMENT_CHARACTERS = "abcdefghijklmnopqrstuvwxy"


KEYWORDS = {
    'as',
    'define',
    'expose',
    'group',
    'include',
    'ignore'
}

_TOKEN_PRIORITY = [
    LT.STATEMENT,
    LT.RULE
]

# Numbers the statements so statement 0 is now at key 0
TOKEN_PRIORITY = {x[1]: x[0] for x in enumerate(_TOKEN_PRIORITY)}

_UNUSED = "§$%&/=?~:;.,|_@"
