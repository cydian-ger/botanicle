from compiler.Lcompile_file import compile_file
from compiler.lcompiler.bottle import Bottle
import pickle
from pprint import pprint


if __name__ == '__main__':
    FILE_NAME = "test/test.l"
    OUT_NAME = './test/data'
    file = open(FILE_NAME, encoding="utf-8")
    compile_file(file, OUT_NAME)

    f = open(OUT_NAME, 'rb')
    y: Bottle = pickle.load(f)
    f.close()
    pprint(y)
