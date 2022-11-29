import sys
from typing import Tuple

from colorama import Back, Style, Fore

from compiler.lexer.static import LINE_BREAK

Compiler = sys.modules[__name__]

Compiler.string = None
Compiler.err_padding = None


def init_compiler(string: str):
    if Compiler.string is None:
        Compiler.string = string
        Compiler.err_padding = 2
    else:
        raise RuntimeError("Variable already defined")


def char(str_left: str):
    # str_left is the amount of string that is left
    return len(Compiler.string) - len(str_left)


def lraise(error: BaseException, err_pos: Tuple[int, int]):
    file_text = Compiler.string.split(LINE_BREAK)
    for index, line in enumerate(file_text):
        line: str
        file_text[index] = line + "\n"

    index = 0
    line_start_index = list()
    for line in file_text:
        index += len(line)
        line_start_index.append(index)

    del index

    fault_line_index = len([x for x in line_start_index if x < err_pos[0]])
    fault_line = file_text[fault_line_index]

    if fault_line_index > 0:
        in_line_index = (err_pos[0] - line_start_index[fault_line_index - 1],
                         err_pos[1] - line_start_index[fault_line_index - 1])
    else:
        in_line_index = (err_pos[0], err_pos[1])

    print(Fore.RED, end="")
    print(f"Line {fault_line_index + 1}: " + repr(error))

    print("─" * len(fault_line))

    print(f"{Style.RESET_ALL}{fault_line[:in_line_index[0]]}"
          f"{Back.LIGHTRED_EX}{fault_line[in_line_index[0]:in_line_index[1]]}{Style.RESET_ALL}"
          f"{fault_line[in_line_index[1]:]}{Fore.RED}", end="")  # End is "" because there is new line at the end

    print("─" * in_line_index[0] +
          "↑" * (in_line_index[1] - in_line_index[0]) +
          "─" * (len(fault_line) - in_line_index[1]))

    print(Style.RESET_ALL, end="")
    exit(1)
