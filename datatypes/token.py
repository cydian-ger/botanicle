class Token(str):
    def __init__(self, value):
        super(Token, self).__init__()
        self.value = value

        if len(self) > 1:
            raise SyntaxError("Token has to have the length of 1")

