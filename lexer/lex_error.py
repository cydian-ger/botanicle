import sys
import inspect
from pprint import pprint


class LexError(BaseException):
    def __init__(self, message: str, string: str, exception=SyntaxError):
        self.message = message
        self.exception = exception
        self.remaining_string = string
        self.caller = inspect.getouterframes(inspect.currentframe(), 2)[1]

    def __repr__(self):
        return str(self)

    def __str__(self):
        error_msg = f'{self.exception.__name__}("{self.message}")'

        gettrace = getattr(sys, 'gettrace', None)
        if gettrace() is not None or sys.argv.__contains__("-debug"):
            return f"{error_msg}\n-debug <origin>: {self.caller[3]}: {self.caller[2]}"

        return error_msg
