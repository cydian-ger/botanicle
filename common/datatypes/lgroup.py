from common.datatypes import Token, Value_List


class Group:
    name: Token
    members: Value_List[Token]

    def __init__(self, name: Token, s):
        self.name = name
        self.members = Value_List(s)

    def __repr__(self):
        return self.name.data

    def __str__(self):
        return repr(self)

    def __iter__(self):
        return iter(self.members)
