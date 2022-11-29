import sys
from common.LError import LError
from compiler.lexer.static import ARGV_DEBUG
from compiler.Lglobal import Compiler


class LexError(LError):
    def __init__(self, message: str, string: str, exception=SyntaxError):
        self.remaining_string = string
        super().__init__(message=message, exception=exception)

    def __repr__(self):
        return str(self)

    def __str__(self):
        error_msg = f'<{self.exception.__name__}>. {self.message}'

        if sys.argv.__contains__(ARGV_DEBUG):
            print(len(Compiler.string))
            return f"{error_msg}\n-debug <error_origin> {self.caller}"

        return error_msg
