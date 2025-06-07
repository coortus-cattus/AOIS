# tests/test_normal_forms.py

import unittest
from parser.logic_parser import parse_expression
from truth_table.generator import generate_truth_table
from normal_forms.builder import build_sdnf, build_sknf

class TestNormalFormsBuilder(unittest.TestCase):
    def setUp(self):
        self._parse_and_generate = lambda expr: generate_truth_table(*parse_expression(expr))

    def test_sdnf_true_or_false(self):
        truth_table = self._parse_and_generate("a | b")
        variables = ['a', 'b']
        sdnf = build_sdnf(truth_table, variables)
        expected_terms = ["a & b", "a & !b", "!a & b"]
        for term in expected_terms:
            self.assertIn(term, sdnf)

    def test_sknf_and(self):
        truth_table = self._parse_and_generate("a & b")
        variables = ['a', 'b']
        sknf = build_sknf(truth_table, variables)
        expected_terms = ["a | b", "a | !b", "!a | b"]
        for term in expected_terms:
            self.assertIn(term, sknf)


if __name__ == '__main__':
    unittest.main()
