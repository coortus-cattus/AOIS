import unittest
from utils.expression_utils import get_index_form, get_numeric_form

class MockNode:
    """Простой класс для имитации логического дерева."""
    def __init__(self, func):
        self.func = func

    def evaluate(self, context):
        return self.func(context)

class TestExpressionUtils(unittest.TestCase):

    def test_get_index_form_basic(self):
        # f(a, b) = a AND b
        root = MockNode(lambda ctx: ctx['a'] and ctx['b'])
        variables = ['a', 'b']
        result = get_index_form(root, variables)
        self.assertEqual(result, '0001')  # только последний вариант True

    def test_get_index_form_full_output(self):
        root = MockNode(lambda ctx: ctx['a'] or ctx['b'])
        variables = ['a', 'b']
        result = get_index_form(root, variables, full_output=True)
        expected = [('00', 0), ('01', 1), ('10', 1), ('11', 1)]
        self.assertEqual(result, expected)

    def test_get_numeric_form_sdnf(self):
        # f(a, b) = a XOR b
        root = MockNode(lambda ctx: ctx['a'] != ctx['b'])
        variables = ['a', 'b']
        result = get_numeric_form(root, variables, mode='sdnf')
        self.assertEqual(result, [1, 2])  # 01 и 10

    def test_get_numeric_form_sknf(self):
        # f(a, b) = a XOR b
        root = MockNode(lambda ctx: ctx['a'] != ctx['b'])
        variables = ['a', 'b']
        result = get_numeric_form(root, variables, mode='sknf')
        self.assertEqual(result, [0, 3])  # 00 и 11

if __name__ == '__main__':
    unittest.main()
