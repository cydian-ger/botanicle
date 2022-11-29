from typing import List, Optional, Union, Dict, Tuple, Any

from compiler.bottle import Bottle
from common.datatypes import Name, Value_List, Expression
from common.iterator.LMatch import LMatch
from common.iterator.rule import Rule
from compiler.lexer.LT import LT
from compiler.lexer.static import CONTEXT_LEFT, CONTEXT_RIGHT
from compiler.Lglobal import lraise


def _compile_lmatch(name, args, argument_class: Union[type(Name), type(Expression)], ac_kwargs: Optional[Dict] = None):
    token_name = name
    token_args = Value_List()
    token_args.set_type(argument_class)
    # Add every argument
    for arg_t, arg_v, arg_i in args:
        if arg_t == LT.ARG or arg_t == LT.EXPR:

            if ac_kwargs:
                token_args.append(argument_class(arg_v, **ac_kwargs))
            else:
                token_args.append(argument_class(arg_v))

        elif arg_t == LT.FUNCTION:
            # Load function
            raise NotImplementedError("Functions as arguments in LTokens are not supported yet")

        else:
            lraise(SyntaxError(f"Invalid Argument Type for Token: {arg_t}."), arg_i)

    return LMatch(token_name, token_args)


def _compile_rule(token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]], bottle: Bottle,
                  line_token: Tuple[LT, Any, Tuple[int, int]]):
    name: Optional[Name] = None
    for token, content, token_index in token_list:
        if token not in {LT.ASSIGNMENT, LT.LTOKEN, LT.ARGS, LT.CONTEXT_TOKEN, LT.CONDITION, LT.RESULT,
                         LT.FUNCTION, LT.FUNCTION_ARGS}:
            lraise(SyntaxError(f"{token} is not an allowed Token in a Rule"), token_index)

        if token is LT.ASSIGNMENT:
            name = Name(content)

    if name is not None:
        if name in bottle.rule_assignments:
            lraise(KeyError(f"Line assignment '{name}' appeared more than once."), line_token[2])

        else:
            bottle.rule_assignments.add(name)

    # Remove the assignment from the list if it exists
    if name is not None:
        token_list.pop(0)

    # If there are no result tokens in the rule raise Error
    if len([_ for _ in token_list if _[0] == LT.RESULT]) == 0:
        lraise(SyntaxError(f"Rule has to contain a result"), line_token[2])

    # Check if there are a valid amount of context tokens and if they are arranged correctly.
    context_tokens = [_ for _ in token_list if _[0] == LT.CONTEXT_TOKEN]
    if len(context_tokens) > 2:
        lraise(SyntaxError(f"Only two context tokens are allowed per rule. {len(context_tokens)} were provided.")
               , context_tokens[2][2])

    elif len(context_tokens) == 2:
        if not context_tokens[0][1] == CONTEXT_LEFT:
            lraise(SyntaxError(f"First context token has to be: '{CONTEXT_LEFT}' but is '{context_tokens[0][1]}'"),
                   context_tokens[0][2])

        if not (context_tokens[1][1] == CONTEXT_RIGHT):
            lraise(SyntaxError(f"Second context token has to be: '{CONTEXT_RIGHT}' but is '{context_tokens[1][1]}'"),
                   context_tokens[1][2])

    # CONTINUE LEXING
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
            ltoken = _compile_lmatch(content[0][1], content[1][1], Name)
            match_list.append(ltoken)

        elif token == LT.CONTEXT_TOKEN:
            match_list.append(LMatch(content, Value_List()))

        elif token == LT.FUNCTION:
            # Use same function as above
            raise NotImplementedError("functions outside of arguments not supported yet")

        # Take the condition
        elif token == LT.CONDITION and content != []:
            con_token, con_content, con_index = content[0]
            # Package conditions as list
            condition = Value_List()
            condition.set_type(Expression)

            if con_token == LT.CON_EXPR:
                condition.append(Expression(con_content, result_type=bool))

            elif con_token == LT.ARGS:
                for con_arg in con_content:
                    condition.append(Expression(con_arg[1], result_type=bool))

        elif token == LT.RESULT:
            # Unpack the result token into the result
            result = Value_List()
            result.set_type(LMatch)

            # Compile and pack all LTokens embedded in the result
            for _, result_content, result_index in content:
                result_token = _compile_lmatch(result_content[0][1], result_content[1][1], Expression,
                                               {"result_type": Union[float, int]})
                result.append(result_token)
        index += 1

    # Split left context
    left_con = LMatch(CONTEXT_LEFT, Value_List())
    if match_list.__contains__(left_con):
        _index = match_list.index(left_con)
        left_context = match_list[:_index]
        match_list = match_list[_index + 1:]

    # Split right context
    right_con = LMatch(CONTEXT_RIGHT, Value_List())
    if match_list.__contains__(right_con):
        _index = match_list.index(right_con)
        right_context = match_list[_index + 1:]
        match_list = match_list[:_index]

    if len(match_list) != 1:
        raise SyntaxError(f"Rule has to have 1 match. Received {len(match_list)} instead.")

    rule = Rule(
        match=match_list[0],
        assignment=name,
        left_context=left_context,
        right_context=right_context,
        condition=condition,
        result=result
    )

    if rule in bottle.rule_list:
        raise SyntaxError(f"There already exists a rule with equivalent match for the rule: '{rule}'")

    for variable in rule.variables:
        if variable in bottle.variables.keys():
            raise KeyError(f"Match Variable '{variable}' overrides defined variable.")

    bottle.rule_list.append(rule)
    # bottle.rule


def compile_rule(token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]], bottle: Bottle,
                 line_token: Tuple[LT, Any, Tuple[int, int]]):
    info = token_list.pop(0)[1]

    _compile_rule(token_list, bottle, line_token)
    """
    except Compile_Error as e:
        raise e
    
    except Exception as e:
        if len(e.args) > 0:
            raise Compile_Error(e.args[0], info, e)
    
        else:
            raise Compile_Error("ERROR MSG MISSING", info, e)"""
