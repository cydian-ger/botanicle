import inspect
import os
import sys

from compiler.lexer.static import ARGV_DEBUG, ARGV_WARNING
from colorama import Fore, Style


def lwarn(warning: Warning):
    if not sys.argv.__contains__(ARGV_WARNING):
        return

    print(f"{Fore.RED}", end="")
    print(f"<{warning.__class__.__name__}> {warning.args[0]}")
    if sys.argv.__contains__(ARGV_DEBUG):
        _caller = inspect.getouterframes(inspect.currentframe(), 3)[1]
        # [2] Because this is a removed function
        print(f"-debug <error_origin>: "
              f"{os.path.basename(_caller[1])} {_caller[3]}(): Line {_caller[2]}")

    print(f"{Style.RESET_ALL}")