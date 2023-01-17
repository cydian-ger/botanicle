import unittest
from typing import Optional
import os

from common.common_names import COMPILED_FORMAT
from compiler.Lcompile_file import compile_file
from compiler.Lglobal.compiler_global import reset_compiler
from production.Lglobal.production_global import reset_production
from production.Lproduction import production
from production.static.lines import Line

FILE_NAME = "test"


def load(file, kwargs: Optional[dict] = None):
    TestProduction.currentFile = file
    file = file + FILE_NAME
    compile_file(file)
    production(file, kwargs)


class TestProduction(unittest.TestCase):
    currentFile: str = ""

    def setUp(self) -> None:
        reset_compiler()
        reset_production()

    def tearDown(self) -> None:
        # Remove the compiled file
        file = TestProduction.currentFile + FILE_NAME + COMPILED_FORMAT
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
        TestProduction.currentFile = None

    def test_generic(self):
        load("./test_dir/test_generic/", {"max_iter": 2})
        self.assertEqual(Line.print(), "ABBBBBBBBA")

    def test_context(self):
        load("./test_dir/test_generic_2/", {"max_iter": 5})
        self.assertEqual(Line.print(), "B(1.0)")

    def test_context_ignore(self):
        load("./test_dir/test_context_ignore/", {"max_iter": 2})
        self.assertEqual(Line.print(), "A(2.0)Z(1.0)X(1.0)Z(1.0)B(2.0)")

    def test_context_retrieval(self):
        load("./test_dir/test_context_retrieval/", {"max_iter": 2})
        self.assertEqual(Line.print(), "A(1.0)A(1.0)A(1.0)")
