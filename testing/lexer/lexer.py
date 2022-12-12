import unittest

from compiler.lexer.LT import LT
from compiler.lexer.lex import lex


# All Lexer Errors
class TestLexer(unittest.TestCase):
    # TODO
    def test_ltoken(self):
        name, arg = ("A", "b")
        test_string = f"{name}({arg})"
        tokens = lex(test_string)
        self.assertEqual(tokens[1][0], LT.LTOKEN)
        self.assertEqual(tokens[2][1], name)
        self.assertEqual(tokens[3][0], LT.ARGS)
        self.assertEqual(tokens[4][1], arg)
        self.assertEqual(tokens[5][0], LT.ARGS_END)
