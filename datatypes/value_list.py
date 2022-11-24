class Value_List(list):
    _type: type = None

    def append(self, __object) -> None:
        if self._type is not None:
            if not isinstance(__object, self._type):
                raise SyntaxError(f"Every object added has to be of the type <{self._type.__name__}>")

        super().append(__object)

    def set_type(self, _type: type):
        self._type = _type
