

class LexError(BaseException):
    def __init__(self, message: str, string: str, exception=SyntaxError):
        self.message = message
        self.exception = exception
        self.remaining_string = string

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.exception.__name__}("{self.message}")'
