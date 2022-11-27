import sys

from colorama import Fore, Style
from typing import Optional, Tuple
import inspect

from lexer.static import ARGV_DEBUG


class LWarning:
    def __init__(self, message: str, warning = Warning, caller: Optional[Tuple[str, str]] = None):
        self.message = message
        self.warning = warning

        if caller is None:
            _caller = inspect.getouterframes(inspect.currentframe(), 3)[2]  # [2] Because this is base class
            self.caller_name = _caller[3]
            self.caller_line = _caller[2]
        else:
            # If another error instance is packed into the error wrapper: trace that error back instead of this class
            self.caller_name, self.caller_line = caller

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        warning_msg = f"<{self.warning.__name__}> {self.message}"

        if sys.argv.__contains__(ARGV_DEBUG):
            warning_msg = f"{warning_msg}\n-debug <error_origin> ({self.caller_name}: {self.caller_line})"

        return f"{Fore.RED}{warning_msg}{Style.RESET_ALL}"

    def throw(self):
        print(self)
