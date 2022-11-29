from typing import List, Tuple, Any, Union
from compiler.lexer.LT import LT
from compiler.lexer.lex_statement import lex_statement
from compiler.lexer.lex_comment import lex_comment
from compiler.lexer.lex_linebreak import lex_linebreak
from compiler.lexer.lex_rule import lex_rule
from compiler.lexer.static import LINE_BREAK, VALID_STATEMENT_CHARACTERS, VALID_RULE_START
from compiler.Lglobal import char


def _line_info(string: str, index: int, token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]]):
    line_number = string[:index].count("\n") + 1
    line = string.split("\n")[line_number - 1]
    token_list.append((LT.INFO, {"line_number": line_number, "line_text": line}, char(string[index:])))


def lex(string: str):
    # If any definition block has been opened and not yet closed its put here
    token_list: List[Tuple[LT, Any, Union[int, Tuple[int, int]]]] = list()

    index = 0
    while index < len(string):
        c = string[index]
        # Skip new lines
        if c == LINE_BREAK:
            index += lex_linebreak(string[index:], token_list)

        elif c in VALID_STATEMENT_CHARACTERS:
            token_list.append((LT.STATEMENT, None, char(string[index:])))
            _line_info(string, index, token_list)
            index += lex_statement(string[index:], token_list)

        elif c == "#":
            index += lex_comment(string[index:], token_list)

        elif c in VALID_RULE_START:
            token_list.append((LT.RULE, None, char(string[index:])))
            _line_info(string, index, token_list)
            index += lex_rule(string[index:], token_list)

        else:
            index += 1
    return token_list


