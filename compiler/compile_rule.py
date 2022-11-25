from typing import List, Tuple, Any, Optional

from compiler.bottle import Bottle
from compiler.compile_error import Compile_Error
from datatypes import Name, Token, Value_List, Expression
from iterator.Ltoken import LToken
from iterator.context import Context
from lexer.LT import LT


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

        if name is not None:
            token_list.pop(0)

        # If there are no result tokens in the rule raise Error
        if len([_ for _ in token_list if _[0] == LT.RESULT]) == 0:
            raise SyntaxError(f"Rule has to contain a result")

        # CONTINUE LEXING

        left_context: Optional[List[Context]] = None
        right_context: Optional[List[Context]] = None
        lmatch: Optional[Token] = None
        condition: Optional[Value_List[Expression]] = None
        # Match part
        index = 0

        held_list: List[LToken] = list()

        while index < len(token_list):
            token, content = token_list[index]

            if token == LT.LTOKEN:
                ltoken_name = content
                ltoken_args = Value_List()

                if (index + 1) < len(token_list):
                    if token_list[index + 1][0] == LT.ARGS:
                        for ltoken_arg in token_list[index + 1][1]:
                            if ltoken_arg[0] == LT.ARG:
                                ltoken_args.append(Name(ltoken_arg[1]))

                            elif ltoken_arg[0] == LT.FUNCTION:
                                # call a function that resolves mulitple arguments
                                raise NotImplementedError("functions inside of arguments not supported yet")

                            elif ltoken_arg[0] == LT.ARGS:
                                raise SyntaxError("Nested arguments are not allowed")

                        index += 1

                held_list.append(LToken(ltoken_name, ltoken_args))

            elif token == LT.FUNCTION:
                # Use same function as above
                raise NotImplementedError("functions outside of arguments not supported yet")

            # Take the condition
            elif token == LT.CONDITION:
                con_token, con_content = content[0]
                # Package conditions as list
                condition = Value_List()
                condition.set_type(Expression)

                if con_token == LT.CON_EXPR:
                    condition.append(Expression(con_content))

                elif con_token == LT.ARGS:
                    for con_arg in con_content:
                        condition.append(Expression(con_arg[1]))

            elif token == LT.RESULT:
                res_token, res_content = content[0]
                result = Value_List()
                result.set_type(LToken)

            index += 1

    except Compile_Error as e:
        raise e

    except Exception as e:
        if len(e.args) > 0:
            raise Compile_Error(e.args[0], info, e)

        else:
            raise Compile_Error("ERROR MSG MISSING", info, e)

    # F < F > F : con -> F
    # F < F : con -> F
    # F > F : con -> F
    # F : con -> F
    # F : -> F
    # F -> F
    # : con -> F
    # -> F
