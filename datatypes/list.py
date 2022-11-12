class List(list):
    _locked: bool = False
    _type: type = None

    def append(self, __object) -> None:
        if self._type is None:
            self._type = type(__object)
        else:
            if not isinstance(__object, self._type):
                raise SyntaxError("Every object added has to be of this type")

        super().append(__object)

    def lock(self):
        self._locked = True
