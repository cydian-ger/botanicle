import sys

from common.env import env_args
from compiler.Lglobal.ltrace import ltrace
from compiler.lexer.static import ARGV_DEBUG, ARGV_WARNING, ARGV_TEST
from colorama import Fore, Style


def lwarn(warning: Warning):
    if env_args.__contains__(ARGV_TEST):
        raise warning

    if not env_args.__contains__(ARGV_WARNING):
        return

    print(f"{Fore.RED}", end="")
    print(f"<{warning.__class__.__name__}> {warning.args[0]}")
    if env_args.__contains__(ARGV_DEBUG):
        print(ltrace(stack_limit=3))

    print(f"{Style.RESET_ALL}")
