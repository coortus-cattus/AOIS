import unittest
from parser.logic_parser import parse_expression

class TestLogicParser(unittest.TestCase):
    def test_single_variable(self):
        expr = "a"
        root, variables = parse_expression(expr)
        self.assertEqual(variables, ["a"])
        self.assertEqual(root.evaluate({"a": True}), True)
        self.assertEqual(root.evaluate({"a": False}), False)

    def test_not_operator(self):
        expr = "!a"
        root, variables = parse_expression(expr)
        self.assertEqual(variables, ["a"])
        self.assertEqual(root.evaluate({"a": True}), False)
        self.assertEqual(root.evaluate({"a": False}), True)

    def test_and_operator(self):
        expr = "a & b"
        root, variables = parse_expression(expr)
        self.assertEqual(set(variables), {"a", "b"})
        self.assertEqual(root.evaluate({"a": True, "b": True}), True)
        self.assertEqual(root.evaluate({"a": True, "b": False}), False)

    def test_or_operator(self):
        expr = "a | b"
        root, variables = parse_expression(expr)
        self.assertEqual(set(variables), {"a", "b"})
        self.assertEqual(root.evaluate({"a": False, "b": False}), False)
        self.assertEqual(root.evaluate({"a": False, "b": True}), True)

    def test_impl_operator(self):
        expr = "a -> b"
        root, variables = parse_expression(expr)
        self.assertEqual(set(variables), {"a", "b"})
        self.assertEqual(root.evaluate({"a": True, "b": False}), False)
        self.assertEqual(root.evaluate({"a": True, "b": True}), True)
        self.assertEqual(root.evaluate({"a": False, "b": False}), True)

    def test_equiv_operator(self):
        expr = "a ~ b"
        root, variables = parse_expression(expr)
        self.assertEqual(set(variables), {"a", "b"})
        self.assertEqual(root.evaluate({"a": True, "b": True}), True)
        self.assertEqual(root.evaluate({"a": True, "b": False}), False)

    def test_complex_expression(self):
        expr = "(a & !b) | (c -> d)"
        root, variables = parse_expression(expr)
        self.assertEqual(set(variables), {"a", "b", "c", "d"})
        env = {"a": True, "b": False, "c": False, "d": True}
        self.assertEqual(root.evaluate(env), True)

    def test_syntax_error(self):
        expr = "(a & b"
        with self.assertRaises(SyntaxError):
            parse_expression(expr)

if __name__ == '__main__':
    unittest.main()
