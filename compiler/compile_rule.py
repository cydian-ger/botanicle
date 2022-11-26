from typing import List, Optional, Union, Dict, Tuple, Any

from compiler.bottle import Bottle
from compiler.compile_error import Compile_Error
from datatypes import Name, Value_List, Expression
from iterator.Ltoken import LToken
from iterator.rule import Rule
from lexer.LT import LT
from lexer.static import CONTEXT_LEFT, CONTEXT_RIGHT


def _compile_ltoken(name, args, argument_class: Union[type(Name), type(Expression)], ac_kwargs: Optional[Dict] = None):
    token_name = name
    token_args = Value_List()
    token_args.set_type(argument_class)
    # Add every argument
    for arg_t, arg_v in args:
        if arg_t == LT.ARG:

            if ac_kwargs:
                token_args.append(argument_class(arg_v, **ac_kwargs))
            else:
                token_args.append(argument_class(arg_v))

        elif arg_t == LT.FUNCTION:
            # Load function
            raise NotImplementedError("functions as arguments in LTokens are not supported yet")

        else:
            raise SyntaxError(f"Invalid Argument Type for Token: {arg_t}.")

    return LToken(token_name, token_args)


def compile_rule(token_list: List[Tuple[LT, Any]], bottle: Bottle):
    name: Optional[Name] = None
    info = token_list.pop(0)[1]

    try:
        for token, content in token_list:
            if token not in {LT.ASSIGNMENT, LT.LTOKEN, LT.ARGS, LT.CONTEXT_TOKEN, LT.CONDITION, LT.RESULT,
                             LT.FUNCTION, LT.FUNCTION_ARGS}:
                raise SyntaxError(f"{token} is not an allowed Token in a Rule")

            if token is LT.ASSIGNMENT:
                name = Name(content)

        if name is not None:
            if name in bottle.rule_assignments:
                raise KeyError(f"Line assignment '{name}' appeared more than once.")

            else:
                bottle.rule_assignments.add(name)

        # Remove the assignment from the list if it exists
        if name is not None:
            token_list.pop(0)

        # If there are no result tokens in the rule raise Error
        if len([_ for _ in token_list if _[0] == LT.RESULT]) == 0:
            raise SyntaxError(f"Rule has to contain a result")

        # Check if there are a valid amount of context tokens and if they are arranged correctly.
        context_tokens = [_[1] for _ in token_list if _[0] == LT.CONTEXT_TOKEN]
        if len(context_tokens) > 2:
            raise SyntaxError(f"Only two context tokens are allowed per rule. {len(context_tokens)} were provided ("
                              f"{context_tokens}).")

        elif len(context_tokens) == 2:
            if context_tokens[0] == context_tokens[1]:
                raise SyntaxError(f"Context tokens must be different.")

            if not (context_tokens[0] == CONTEXT_LEFT and context_tokens[1] == CONTEXT_RIGHT):
                raise SyntaxError(f"Context tokens must be in order '{CONTEXT_LEFT}', '{CONTEXT_RIGHT}'")

        # CONTINUE LEXING
        left_context: Optional[List[LToken]] = None
        right_context: Optional[List[LToken]] = None
        match_list: List[LToken] = list()
        condition: Optional[Value_List[Expression]] = None
        result: Optional[Value_List[LToken]] = None
        # Match part
        index = 0

        while index < len(token_list):
            token, content = token_list[index]

            if token == LT.LTOKEN:
                ltoken = _compile_ltoken(content[0][1], content[1][1], Name)
                match_list.append(ltoken)

            elif token == LT.CONTEXT_TOKEN:
                match_list.append(LToken(content, Value_List()))

            elif token == LT.FUNCTION:
                # Use same function as above
                raise NotImplementedError("functions outside of arguments not supported yet")

            # Take the condition
            elif token == LT.CONDITION and content != []:
                con_token, con_content = content[0]
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
                result.set_type(LToken)

                # Compile and pack all LTokens embedded in the result
                for _, result_content in content:
                    result_token = _compile_ltoken(result_content[0][1], result_content[1][1], Expression,
                                                   {"result_type": Union[float, int]})
                    result.append(result_token)
            index += 1

        # Split left context
        left_con = LToken(CONTEXT_LEFT, Value_List())
        if match_list.__contains__(left_con):
            _index = match_list.index(left_con)
            left_context = match_list[:_index]
            match_list = match_list[_index + 1:]

        # Split right context
        right_con = LToken(CONTEXT_RIGHT, Value_List())
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
            raise SyntaxError(f"Equivalent rule already defined: '{rule}'")

        bottle.rule_list.append(rule)
        # bottle.rules

    except Compile_Error as e:
        raise e

    except Exception as e:
        if len(e.args) > 0:
            raise Compile_Error(e.args[0], info, e)

        else:
            raise Compile_Error("ERROR MSG MISSING", info, e)
