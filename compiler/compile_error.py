from common.LError import LError
from typing import Any


class Compile_Error(LError):
    def __init__(self, message: str, info: Any, exception=SyntaxError, caller=None):
        super().__init__(message, exception, caller)

        self.info = info
        if exception is type(type):
            super().__init__(message, exception)
        else:
            # Exception is an instance
            super().__init__(message, exception=type(exception),
                             caller=(
                                 str(exception.__traceback__.tb_next.tb_frame.f_code.co_name),
                                 str(exception.__traceback__.tb_next.tb_frame.f_lineno)
                             )
                             )
        #
