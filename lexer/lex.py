from typing import List, Tuple, Any
from lexer.LT import LT
from lexer.lex_error import LexError
from lexer.lex_statement import lex_statement
from lexer.lex_comment import lex_comment
from lexer.lex_linebreak import lex_linebreak
from lexer.lex_rule import lex_rule
from lexer.static import LINE_BREAK, VALID_STATEMENT_CHARACTERS, VALID_RULE_START
from colorama import Fore, Style, Back


def _line_info(string: str, index: int, token_list):
    line_number = string[:index].count("\n") + 1
    line = string.split("\n")[line_number - 1]
    token_list.append((LT.INFO, {"line_number": line_number, "line_text": line}))


def lex(string: str):
    try:
        # If any definition block has been opened and not yet closed its put here
        token_list: List[Tuple[LT, Any]] = list()

        index = 0
        while index < len(string):
            char = string[index]
            # Skip new lines
            if char == LINE_BREAK:
                index += lex_linebreak(string[index:], token_list)

            elif char in VALID_STATEMENT_CHARACTERS:
                token_list.append((LT.STATEMENT, None))
                _line_info(string, index, token_list)
                index += lex_statement(string[index:], token_list)

            elif char == "#":
                index += lex_comment(string[index:], token_list)

            # elif char in SPECIAL_AXIOMS:
            #     raise NotImplementedError
            # Concretely define special axiom behaviour

            elif char in VALID_RULE_START:
                token_list.append((LT.RULE, None))
                _line_info(string, index, token_list)
                index += lex_rule(string[index:], token_list)

            else:
                index += 1

    # Print error
    except LexError as e:
        # Cosmetic variables
        fault_line_cushion = 2

        # print(repr(e))
        fault_index = len(string) - len(e.remaining_string)

        # Store the char index of every line break
        # If the linebreak index is greater than fault index we know its inbetween the lines
        line_breaks: List[int] = [0]

        for index, char in enumerate(string):
            if char == LINE_BREAK:
                line_breaks.append(index)

            if line_breaks[-1] >= fault_index:
                break

        fault_line_index = len(line_breaks) - 2  # Minus two cause first break is set at 0

        lines = string.split(LINE_BREAK)
        for line in lines:
            line += LINE_BREAK

        pre_fault_line_char_total = sum(len(s) + 1 for s in lines[:fault_line_index])  # Add length lines
        # because "\n" are stripped

        fault_line = lines[fault_line_index]
        in_line_index = fault_index - pre_fault_line_char_total

        #
        if string[fault_index] == LINE_BREAK:
            in_line_index -= 1

        print(Fore.RED + f"Line {fault_line_index + 1}: " + repr(e) + Style.RESET_ALL)

        for index, line in enumerate(lines):
            if index == fault_line_index:
                # Puts the upper bound box
                print(Fore.RED + "─" * len(fault_line) + Style.RESET_ALL)
                # Prints the line and highlights the fault in Red

                print(line[:in_line_index] +
                      Back.LIGHTRED_EX + line[in_line_index] + Style.RESET_ALL
                      + line[in_line_index + 1:])
                # Prints the lower bound box plus the error indication arrow
                print(Fore.RED + "─" * in_line_index + "↑" + "─"
                      * (len(fault_line) - in_line_index - 1) + Style.RESET_ALL)
            else:
                if fault_line_cushion:
                    if abs(index - fault_line_index) <= fault_line_cushion:
                        print(line)
        exit(1)
        return

    return token_list


