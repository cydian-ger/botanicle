import unittest
from common.env import env_args
from compiler.Lglobal import init_compiler
from compiler.lexer.static import ARGV_DEBUG, ARGV_TEST, ARGV_WARNING
from testing.LTest import *


if __name__ == '__main__':
    announce()
    init_compiler(" ")
    env_args += [ARGV_DEBUG, ARGV_TEST, ARGV_WARNING]
    unittest.main()
