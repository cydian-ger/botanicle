import sys
from typing import Union, Tuple

from compiler.Lglobal import Compiler
from compiler.Lglobal.ltrace import ltrace
from compiler.lexer.static import LINE_BREAK, ARGV_DEBUG

from colorama import Fore, Back, Style


def lraise(error: BaseException, err_pos: Union[int, Tuple[int, int]], debug_info: str = ""):
    if isinstance(err_pos, int):
        err_pos = (err_pos, err_pos + 1)

    file_text = Compiler.string.split(LINE_BREAK)
    for index, line in enumerate(file_text):
        line: str
        file_text[index] = line + " "  # Space instead of breakline

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

    if sys.argv.__contains__(ARGV_DEBUG):
        if debug_info:
            print(debug_info)
        print(ltrace())

    fault_line_name = f"{fault_line_index + 1}: "
    print("─" * (len(fault_line) + len(fault_line_name)))

    print(f"{Style.RESET_ALL}{fault_line_name}{fault_line[:in_line_index[0]]}"
          f"{Back.LIGHTRED_EX}{fault_line[in_line_index[0]:in_line_index[1]]}{Style.RESET_ALL}"
          f"{fault_line[in_line_index[1]:]}{Fore.RED}")

    print("─" * (in_line_index[0] + len(fault_line_name)) +
          "↑" * (in_line_index[1] - in_line_index[0]) +
          "─" * (len(fault_line) - in_line_index[1]))

    print(Style.RESET_ALL, end="")
    exit(1)
