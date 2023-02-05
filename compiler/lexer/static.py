from compiler.lexer.LT import LT

LINE_BREAK: str = "\n"
EXPR = '"'
ARG_OPEN = "("
ARG_CLOSE = ")"
ARG_DELIMITER = ","  # For A(1, b)
COMMENT = "#"
SPACE = " "
PATH_CHARS = "/."  # For paths and files
EMPTY_ARGUMENT = "_"

# > (e.g. c_ignore)
CONTEXT_LEFT = "<"
CONTEXT_RIGHT = ">"
CONTEXT_TOKENS = CONTEXT_LEFT + CONTEXT_RIGHT
CONDITION_TOKEN = ":"
RESULT_TOKEN = "→"
ASSIGNMENT_TOKEN = "."  # Assign a name to a rule
FUNCTION_TOKEN = "$"
FUNCTION_ATTRIBUTE_TOKEN = "."
REFERENCE_TOKEN = "@"

BASE_AXIOMS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CONTEXT_HINTS = "01234567889"
SPECIAL_AXIOMS = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"  # All of these are greek letters
# Limitation: these can only be used when
# a) referencing an include file
# b) for a catch group (that one only has file wide scope)

__ = "αβγδεζηθικλμνξοπρσςτυφχψω"

# All stack operators
STACK_PUSH = "["
STACK_POP = "]"
STACK_TOKENS = STACK_POP + STACK_PUSH

# All Rotation Things
PITCH_RIGHT = "+"
PITCH_LEFT = "-"
PITCH = PITCH_LEFT + PITCH_RIGHT

# NOT NAMES / SYMBOLS CHOSEN YET
YAW_LEFT = ""
YAW_RIGHT = ""
YAW = YAW_LEFT + YAW_RIGHT

# ROLL
ROLL_LEFT = ""
ROLL_RIGHT = ""
ROLL = ROLL_LEFT + ROLL_RIGHT

ROTATION_TOKENS = PITCH + YAW + ROLL

# Pen Tokens
PEN_UP = "^"
PEN_DOWN = "°"
PEN_TOKENS = PEN_UP + PEN_DOWN

# Brush Tokens
BRUSH_INCREASE_SIZE = ""
BRUSH_DECREASE_SIZE = ""
BRUSH_TOKENS = BRUSH_INCREASE_SIZE + BRUSH_DECREASE_SIZE

PRODUCTION_RULES = "{}" + STACK_TOKENS + PITCH + PEN_TOKENS

GENERIC = "*"
MATCH_RETRIEVAL = "?"

# All tokens that can be used in rules A, *, [, ]
VALID_RULE_LTOKENS = BASE_AXIOMS + PRODUCTION_RULES + GENERIC + SPECIAL_AXIOMS + CONTEXT_HINTS + MATCH_RETRIEVAL

# For the .start
VALID_START_TOKENS = BASE_AXIOMS + PRODUCTION_RULES + CONTEXT_HINTS

# Valid tokens that can appear in a result
VALID_RESULT_TOKENS = BASE_AXIOMS + PRODUCTION_RULES + CONTEXT_HINTS + MATCH_RETRIEVAL


# Valid characters that denote the start of a rule
VALID_RULE_START = VALID_RULE_LTOKENS + CONDITION_TOKEN + ASSIGNMENT_TOKEN + FUNCTION_TOKEN

VALID_STATEMENT_CHARACTERS = "abcdefghijklmnopqrstuvwxy"

START_RULE = "start"


class KW:
    alias = 'as'
    define = 'define'
    expose = 'expose'
    group = 'group'
    include = 'include'
    ignore = 'ignore'
    lwith = 'with'  # Called lwith cause with is a keyword in python


KEYWORDS = {var for key, var in vars(KW).items() if not key.startswith("__")}

FRAME_KEYWORDS = {
    KW.include,
    KW.expose
}

_TOKEN_PRIORITY = [
    LT.STATEMENT,
    LT.RULE
]

# Numbers the statement so statement 0 is now at key 0
TOKEN_PRIORITY = {x[1]: x[0] for x in enumerate(_TOKEN_PRIORITY)}

ARGV_TEST = "-test"
ARGV_LINT = "-lint"
ARGV_DEBUG = "-debug"
ARGV_WARNING = "-warning"
