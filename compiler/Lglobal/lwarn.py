import sys

from compiler.Lglobal.ltrace import ltrace
from compiler.lexer.static import ARGV_DEBUG, ARGV_WARNING
from colorama import Fore, Style


def lwarn(warning: Warning):
    if not sys.argv.__contains__(ARGV_WARNING):
        return

    print(f"{Fore.RED}", end="")
    print(f"<{warning.__class__.__name__}> {warning.args[0]}")
    if sys.argv.__contains__(ARGV_DEBUG):
        print(ltrace(stack_limit=3))

    print(f"{Style.RESET_ALL}")
