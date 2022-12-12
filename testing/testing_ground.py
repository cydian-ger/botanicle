from typing import Union

from common.datatypes import Expression
from common.iterator.objects import Turtle, LIterator
from compiler.lexer.static import ARGV_TEST, ARGV_DEBUG, ARGV_WARNING
from common.env import env_args

if __name__ == '__main__':
    env_args += [ARGV_DEBUG, ARGV_TEST, ARGV_WARNING]
    