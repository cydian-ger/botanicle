from common.datatypes import Expression
from common.iterator.objects import Turtle, LIterator
from compiler.lexer.static import ARGV_TEST, ARGV_DEBUG, ARGV_WARNING
from common.env import env_args

if __name__ == '__main__':
    env_args += [ARGV_DEBUG, ARGV_TEST, ARGV_WARNING]
    e = Expression("LIterator.stack_size", (0, 0), result_type=int)
    LIterator.stack.append("a")
    Turtle.x += 1.0
    print(e.evaluate({"a": 10000}))
