import unittest

from typing import Union

from common.datatypes import Expression


# Test Compiler things
from common.iterator.objects import LIterator, Turtle


class TestCompiler(unittest.TestCase):
    def test_expression(self):
        # Check if loading
        expr = "LIterator.stack_size + Turtle.x + seed(1.0, 1.0, 1) + a"
        e = Expression(expr, (0, 0), result_type=Union[int, float])
        LIterator.stack.append("a")
        Turtle.x += 1.0
        self.assertEqual(e.evaluate({"a": 1.0}), 4.0)
        e = Expression(expr, (0, 0), result_type=Union[int, float])
        LIterator.stack.pop()
        Turtle.x += 1.5
        self.assertEqual(e.evaluate({"a": 10}), 13.5)
