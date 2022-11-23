from typing import List, Tuple, Any

from compiler.compile_error import Compile_Error
from compiler.compile_statement import compile_statement
from lexer.LT import LT
from colorama import Fore, Style


# This compiles a single file
def l_compile(token_list: List[Tuple[LT, Any]]):
    try:
        for token, content in token_list:
            content: List[Tuple[LT, Any]]

            match token:
                case LT.STATEMENT:
                    compile_statement(content, None)

                case LT.RULE:
                    pass

                case LT.COMMENT:
                    # Comments are skipped for now
                    continue

    except Compile_Error as e:
        print(f"{Fore.RED}"
              f"Line {e.info['line_number']}: {repr(e)}"
              f"{Style.RESET_ALL}")
