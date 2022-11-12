from enum import Enum, auto


class LT(Enum):
    def __repr__(self):
        return str(self)

    # Args
    ARG = auto(), # A('1')
    ARGS = auto(),  # A'('1)
    ARGS_END = auto(),  # A(1')'

    # #comment
    COMMENT = auto(),  # '#'

    NEW_LINE = auto(),  # \n

    # L TOKENS
    RULE = auto(),  # Symbols the start of a rule

    ASSIGNMENT = auto(),  # Used to give a rule a name so it can be referenced later

    # LToken A
    LTOKEN = auto(),  # 'A', 'B'

    CONTEXT_TOKEN = auto(),  # '<', '>'

    FUNCTION = auto(),
    FUNCTION_ARGS = auto(),
    FUNCTION_ARGS_END = auto(),
    # List
    # OPEN_ARGS = auto,  # '('
    # CLOSE_ARGS = auto,  # ')'
    # Everything inside the list is simply split by the comma

    # Everything that is taken as the condition for a rule
    CONDITION = auto(),  # ': .. ' =>
    CONDITION_END = auto(),
    CON_EXPR = auto(),  # arguments in the condition part

    # Result of a rule
    RESULT = auto(),  # '=>'
    RESULT_END = auto(),

    # 1. STATEMENTS
    # 1.1 Building blocks:
    STATEMENT = auto(),

    # 1.2 Keywords
    KEYWORD = auto(),

    NAME = auto(),

    VALUE = auto(),


# Given an open start block, gives the ending block for said block
LT_CLOSE = {
    LT.STATEMENT: LT.NEW_LINE,

    LT.ARGS: LT.ARGS_END,
    LT.FUNCTION_ARGS: LT.FUNCTION_ARGS_END,

    LT.RULE: LT.NEW_LINE,
    LT.CONDITION: LT.CONDITION_END,
    LT.RESULT: LT.RESULT_END,
}
