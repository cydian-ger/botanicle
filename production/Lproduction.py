import pickle

from common.common_names import EDITOR_FORMAT, COMPILED_FORMAT
from compiler.lcompiler.bottle import Bottle
from production.Lglobal.production_global import *


def production(name: str):
    try:
        f = open(name + COMPILED_FORMAT, 'rb')
        bottle: Bottle = pickle.load(f)
        init_production({"max_iter": 100}, bottle)
        f.close()

        # Load the bottle
        # Iterate over the write-string and the out-string.
        # .

    except KeyboardInterrupt:
        # TODO do things
        pass
    except Exception as e:
        print(repr(e))
