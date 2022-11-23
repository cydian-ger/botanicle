import sys
import inspect
from typing import Optional, Tuple


class LError(BaseException):
    def __init__(self, message: str, exception=SyntaxError, caller: Optional[Tuple[str, str]] = None):
        self.message = message
        self.exception = exception

        if caller is None:
            _caller = inspect.getouterframes(inspect.currentframe(), 3)[2]  # [2] Because this is base class
            self.caller_name = _caller[3]
            self.caller_line = _caller[2]
        else:
            # If another error instance is packed into the error wrapper: trace that error back instead of this class
            self.caller_name, self.caller_line = caller

    def __repr__(self):
        return str(self)

    def __str__(self):
        # error_msg = f'{self.exception.__name__}("{self.message}")'
        error_msg = f'<{self.exception.__name__}>. {self.message}'

        if sys.argv.__contains__("-debug"):
            return f"{error_msg}\n-debug <error_origin> ({self.caller_name}: {self.caller_line})"

        return error_msg
