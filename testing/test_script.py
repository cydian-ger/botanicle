import unittest
from common.env import env_args
from compiler.Lglobal import init_compiler
from compiler.lexer.static import ARGV_DEBUG, ARGV_TEST, ARGV_WARNING
from testing.lexer import *


if __name__ == '__main__':
    env_args += [ARGV_DEBUG, ARGV_TEST, ARGV_WARNING]
    unittest.main()
