from typing import List, Optional, Union, Dict, Tuple, Any

from common.datatypes.LResult import LResult
from compiler.lcompiler.bottle import Bottle
from common.datatypes import Name, Value_List, Expression
from common.datatypes.LMatch import LMatch
from compiler.lcompiler.compile_full_rule import compile_full_rule
from compiler.lcompiler.compile_match_token import compile_lmatch
from compiler.lcompiler.compile_named_result import compile_named_result
from compiler.lcompiler.compile_result_token import compile_result_token
from compiler.lexer.LT import LT
from compiler.lexer.static import CONTEXT_LEFT, CONTEXT_RIGHT
from compiler.Lglobal import lraise


def compile_rule(token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]], bottle: Bottle,
                 line_token: Tuple[LT, Any, Tuple[int, int]]):
    name: Optional[Name] = None

    # Check if the rule is composed of valid tokens
    for token, content, token_index in token_list:
        if token not in {LT.ASSIGNMENT, LT.LTOKEN, LT.ARGS, LT.CONTEXT_TOKEN, LT.CONDITION, LT.RESULT,
                         LT.FUNCTION, LT.FUNCTION_ARGS}:
            lraise(SyntaxError(f"{token} is not an allowed Token in a Rule"), token_index)

        # The LTest already checks if the assignment is at the start of a token
        if token is LT.ASSIGNMENT:
            name = Name(content)

    # If an assignment was given to the rule, check if its unique and then add it
    if name is not None:
        if name in bottle.rule_assignments:
            lraise(KeyError(f"Line assignment '{name}' appeared more than once."), line_token[2])
        # If the name is not already predefined add it to the set of names
        bottle.rule_assignments.add(name)

    # Remove the assignment from the list if it exists
    if name is not None:
        token_list.pop(0)

    # If there are no result tokens in the rule raise Error
    if len([_ for _ in token_list if _[0] == LT.RESULT]) == 0:
        print(token_list)
        lraise(SyntaxError(f"Rule has to contain a result"), line_token[2])

    # Check if there are a valid amount of context tokens and if they are arranged correctly.
    context_tokens = [_ for _ in token_list if _[0] == LT.CONTEXT_TOKEN]
    if len(context_tokens) > 2:
        lraise(SyntaxError(f"Only two context tokens are allowed per rule. {len(context_tokens)} were provided.")
               , context_tokens[2][2])

    # Check if the correct amount of context tokens are in a rule
    elif len(context_tokens) == 2:
        # Check if the first context token is a context_left
        if not context_tokens[0][1] == CONTEXT_LEFT:
            lraise(SyntaxError(f"First context token has to be: '{CONTEXT_LEFT}' but is '{context_tokens[0][1]}'"),
                   context_tokens[0][2])

        # Check if the second context token is a context_right
        if not (context_tokens[1][1] == CONTEXT_RIGHT):
            lraise(SyntaxError(f"Second context token has to be: '{CONTEXT_RIGHT}' but is '{context_tokens[1][1]}'"),
                   context_tokens[1][2])

    # Initialize the parts of the rule
    left_context: Optional[List[LMatch]] = None
    right_context: Optional[List[LMatch]] = None
    match_list: List[LMatch] = list()
    condition: Optional[Value_List[Expression]] = None
    result: Optional[Value_List[LMatch]] = None
    # Match part
    index = 0

    while index < len(token_list):
        token, content, token_index = token_list[index]

        if token == LT.LTOKEN:
            ltoken = compile_lmatch(content[0][1], content[1][1], bottle, token_index)
            match_list.append(ltoken)

        elif token == LT.CONTEXT_TOKEN:
            # Insert placeholder LMatches
            match_list.append(LMatch(content, Value_List(), False))

        elif token == LT.FUNCTION:
            # Use same function as above
            lraise(NotImplementedError("Function as LToken are not supported yet"), token_index)

        # Take the condition
        elif token == LT.CONDITION and content != []:
            con_token, con_content, con_index = content[0]
            # Package conditions as list
            condition = Value_List()
            condition.set_type(Expression)

            if con_token == LT.CON_EXPR:
                condition.append(Expression(con_content, con_index, result_type=bool))

            elif con_token == LT.ARGS:
                for con_arg in con_content:
                    condition.append(Expression(con_arg[1], con_index, result_type=bool))

            elif con_token == LT.FUNCTION:
                lraise(NotImplementedError("Function is not implemented for condition argument."), con_index)

        elif token == LT.RESULT:
            # Unpack the result token into the result
            result = Value_List()
            result.set_type(LResult)

            # Compile and pack all LTokens embedded in the result
            for _, result_content, result_index in content:
                result_token = compile_result_token(
                    result_content[0][1],
                    result_content[1][1], bottle,
                    {"result_type": Union[float, int]}, token_index)

                result.append(result_token)
        index += 1

    # TODO change this to not use LMatches anymore
    # Split left context
    left_con = LMatch(CONTEXT_LEFT, Value_List(), False)
    if match_list.__contains__(left_con):
        _index = match_list.index(left_con)
        left_context = match_list[:_index]
        match_list = match_list[_index + 1:]

        if not left_context:
            lraise(SyntaxError(f"Left context needs at least 1 match to be valid"), line_token[2])

    # Split right context
    right_con = LMatch(CONTEXT_RIGHT, Value_List(), False)
    if match_list.__contains__(right_con):
        _index = match_list.index(right_con)
        right_context = match_list[_index + 1:]
        match_list = match_list[:_index]

        if not right_context:
            lraise(SyntaxError(f"Right context needs at least 1 match to be valid"), line_token[2])

    # Check if more than one match was given
    if len(match_list) > 1:
        lraise(SyntaxError(f"Rules can only have 1 match. Received {len(match_list)} instead. ({match_list})."),
               line_token[2])

    # Check if an unassigned rule does not have a match
    if len(match_list) == 0 and not name:
        lraise(SyntaxError(f"Unassigned rules have to have 1 match. Received {len(match_list)} instead."),
               line_token[2])

    # Partial Rule is now NAMED RESULT
    if len(match_list):  # match_list
        compile_full_rule(match_list, name, left_context, right_context, condition, result, bottle, line_token)
    else:
        compile_named_result(name, result, bottle, line_token)
