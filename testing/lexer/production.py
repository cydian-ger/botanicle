import unittest
from typing import Optional

from compiler.Lcompile_file import compile_file
from compiler.Lglobal.compiler_global import reset_compiler
from production.Lglobal.production_global import reset_production
from production.Lproduction import production
from production.static.lines import Line


def load(file, kwargs: Optional[dict] = None):
    file = file + "test"
    compile_file(file)
    production(file, kwargs)


class TestProduction(unittest.TestCase):
    def setUp(self) -> None:
        reset_compiler()
        reset_production()

    def test_generic(self):
        load("./test_dir/test_generic/")
        self.assertEqual(Line.print(), "A B B B B B B B B A ")

    def test_context(self):
        load("./test_dir/test_generic_2/", {"max_iter": 5})
        self.assertEqual(Line.print(), "B(1.0) ")

    def test_context_ignore(self):
        load("./test_dir/test_context_ignore/", {"max_iter": 2})
        self.assertEqual(Line.print(), "A(2.0) Z(1.0) X(1.0) Z(1.0) B(2.0) ")
