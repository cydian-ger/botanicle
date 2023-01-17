import unittest

from compiler.lexer.lex import lex


# All Lexer Errors
class TestLexerException(unittest.TestCase):
    #
    # ARGS
    #
    def test_args_linebreak(self):
        test_string = "A(A, \n"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_args_function_place(self):
        test_string = "A(a$)"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_args_reference_place(self):
        test_string = "A(a@)"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    #
    # ASSIGNMENT
    #
    def test_assignment_multiple_tokens(self):
        test_string = ".a.name"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_assignment_length(self):
        test_string = ". "
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_assignment_invalid_char(self):
        test_string = ".?"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_assignment_linebreak(self):
        test_string = ".\n"
        with self.assertRaises(SyntaxError) as e:
            lex(test_string)

    #
    # CONDITION
    #
    def test_condition_wrapped(self):
        test_string = "A: a == b"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_condition_multiple_tokens(self):
        test_string = "A ::"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    #
    # EXPR
    #
    def test_expr_linebreak(self):
        test_string = 'A("\n'
        with self.assertRaises(SyntaxError):
            lex(test_string)

    #
    # FUNCTION
    #
    def test_function_name_empty(self):
        test_string = "$ "
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_function_linebreak(self):
        test_string = "$a\n"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_function_multiple_tokens(self):
        test_string = "$a$"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_function_invalid_char(self):
        test_string = "$a?"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    #
    # RULE
    #
    def test_rule_assignment(self):
        test_string = "A(1) .name"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_rule_multiple_conditions(self):
        test_string = 'A : "a == b" → :'
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_rule_result_token(self):
        test_string = 'A → A → A'
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_rule_invalid_char(self):
        test_string = "A !"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    #
    # STATEMENT
    #
    def test_statement_arg_preceded(self):
        test_string = "kw A(1)"
        with self.assertRaises(SyntaxError):
            lex(test_string)

    def test_statement_invalid_char(self):
        test_string = "kw ?"
        with self.assertRaises(SyntaxError):
            lex(test_string)
