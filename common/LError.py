import sys
import inspect
from typing import Optional, Tuple

from lexer.static import ARGV_DEBUG


class LError(BaseException):
    def __init__(self, message: str, exception=SyntaxError, caller: Optional[str] = None):
        self.message = message
        self.exception = exception

        if caller is None:
            _caller = inspect.getouterframes(inspect.currentframe(), 3)[2]  # [2] Because this is base class
            self.caller = f"({_caller[3]}: {_caller[2]})"

        else:
            # If another error instance is packed into the error wrapper: trace that error back instead of this class
            self.caller = caller

    def __repr__(self):
        return str(self)

    def __str__(self):
        # error_msg = f'{self.exception.__name__}("{self.message}")'
        error_msg = f'<{self.exception.__name__}>. {self.message}'

        if sys.argv.__contains__(ARGV_DEBUG):
            error_msg = f"{error_msg}\n-debug <error_origin> {self.caller}"

        return error_msg
