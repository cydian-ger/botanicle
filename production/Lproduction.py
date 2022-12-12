import pickle

from common.common_names import COMPILED_FORMAT
from common.iterator.objects import LIterator
from compiler.lcompiler.bottle import Bottle
from production.Lglobal.match_token import match_token
from production.Lglobal.production_global import init_production
from production.static.lines import Line


def production(name: str):
    try:
        f = open(name + COMPILED_FORMAT, 'rb')
        bottle: Bottle = pickle.load(f)
        init_production({"max_iter": 100}, bottle)
        f.close()

        # Create lines
        Line.new(bottle.start)
        # Flush LIterator
        LIterator.flush()
        LIterator.index = 0
        while True:
            if LIterator.index < len(Line.predecessor):
                ltoken = Line.predecessor[LIterator.index]
                # Do the LToken and rule thing
                # Make a Ltoken to instance bake method
                # Make the match work, together with context and allc
                match_token(ltoken, bottle)

                LIterator.index += 1

            else:
                Line.carriage_return()
                break

    except KeyboardInterrupt:
        # TODO do things
        pass

    except Exception as e:
        raise e

    finally:
        pass
