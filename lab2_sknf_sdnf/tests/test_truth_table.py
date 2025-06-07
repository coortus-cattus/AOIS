# tests/test_truth_table.py

import unittest
from parser.logic_parser import parse_expression
from truth_table.generator import generate_truth_table

class TestTruthTableGenerator(unittest.TestCase):
    def test_single_variable(self):
        expr = 'a'
        root, variables = parse_expression(expr)
        table = generate_truth_table(root, variables)
        self.assertEqual(len(table), 2)
        self.assertTrue(all(row['result'] == row['a'] for row in table))

    def test_not_operator(self):
        expr = '!a'
        root, variables = parse_expression(expr)
        table = generate_truth_table(root, variables)
        expected = [True, False]  # for a = False, True
        results = [row['result'] for row in table]
        self.assertEqual(results, expected)

    def test_and_operator(self):
        expr = 'a & b'
        root, variables = parse_expression(expr)
        table = generate_truth_table(root, variables)
        expected = [False, False, False, True]  # a,b: 00,01,10,11
        results = [row['result'] for row in table]
        self.assertEqual(results, expected)

    def test_or_operator(self):
        expr = 'a | b'
        root, variables = parse_expression(expr)
        table = generate_truth_table(root, variables)
        expected = [False, True, True, True]
        results = [row['result'] for row in table]
        self.assertEqual(results, expected)

    def test_complex_expression(self):
        expr = 'a & (!b | c)'
        root, variables = parse_expression(expr)
        table = generate_truth_table(root, variables)
        self.assertEqual(len(table), 8)  # 2^3 combinations
        for row in table:
            a, b, c = row['a'], row['b'], row['c']
            expected_result = a and (not b or c)
            self.assertEqual(row['result'], expected_result)

if __name__ == '__main__':
    unittest.main()
