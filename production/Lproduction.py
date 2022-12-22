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

        # MAX ITERATION
        MAX_ITER = 3

        # Create lines
        Line.new(bottle.start.result)
        # Flush LIterator
        LIterator.flush()
        LIterator.index = 0
        LIterator.counter = 0

        while True:
            for index, ltoken in enumerate(Line.predecessor):
                LIterator.index = index

                # if LIterator.index < len(Line.predecessor):
                # ltoken = Line.predecessor[LIterator.index]

                # Do the LToken and rule thing
                # Make a Ltoken to instance bake method
                # Make the match work, together with context and all
                match_token(ltoken, bottle)

            LIterator.counter += 1
            if LIterator.counter >= MAX_ITER:
                break

            Line.carriage_return()

        # Final out line
        print(Line.print())

    except KeyboardInterrupt:
        # save it
        # TODO do things
        pass

    except Exception as e:
        raise e

    finally:
        pass
