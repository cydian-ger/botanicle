import pickle
from common.common_names import COMPILED_FORMAT
from common.iterator.objects import LIterator
from compiler.lcompiler.bottle import Bottle
from production.Lglobal.match_token import match_token
from production.Lglobal.production_global import init_production, Production
from production.static.lines import Line


def production(name: str, production_settings: dict = None):
    try:
        f = open(name + COMPILED_FORMAT, 'rb')
        bottle: Bottle = pickle.load(f)
        init_production(production_settings or {}, bottle)
        f.close()

        # Create lines
        Line.new(bottle.start.result)
        # Flush LIterator
        LIterator.flush()
        LIterator.index = 0
        LIterator.counter = 0

        while True:
            for index, ltoken in enumerate(Line.predecessor):
                LIterator.index = index

                # Put the token into the rules
                match_token(ltoken, bottle)

            LIterator.counter += 1
            if LIterator.counter >= Production.settings["max_iter"]:
                break

            Line.carriage_return()

        Line.stash()
        # Final out line
        # print(Line.print())

    except KeyboardInterrupt:
        # save it
        # TODO do things
        pass

    except Exception as e:
        raise e

    finally:
        pass
