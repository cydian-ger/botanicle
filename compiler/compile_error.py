import pathlib

from common.LError import LError
from typing import Any, List


class Compile_Error(LError):
    def __init__(self, message: str, info: Any, exception=SyntaxError, caller=None):
        super().__init__(message, exception, caller)

        self.info = info
        if exception is type(type):
            super().__init__(message, exception)
        else:
            # Exception is an instance
            frame = exception.__traceback__
            exception_trace: List[str] = list()

            while frame.tb_next is not None:
                frame = frame.tb_next
                exception_trace.append(f"{pathlib.PurePath(frame.tb_frame.f_code.co_filename).name}"
                                       f"{frame.tb_frame.f_code.co_name}"
                                       f"{frame.tb_frame.f_lineno}")

            super().__init__(message, exception=type(exception),
                             caller=(
                                 "\n\t".join(["Traceback:"] + exception_trace)
                             ))
