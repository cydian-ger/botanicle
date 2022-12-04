class FuncFloat(float):
    def __new__(cls, value):
        return float.__new__(cls, value())


if __name__ == '__main__':
    pass
