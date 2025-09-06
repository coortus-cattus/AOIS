import unittest
from unittest.mock import patch
from minimization.calculation import term_to_bin, bin_to_term, covers_minterm, minimize_sknf_calculation, minimize_sdnf_calculation
from minimization.karnaugh import generate_gray_code, build_karnaugh_map, find_groups, minimize_sknf_karnaugh, minimize_sdnf_karnaugh
from minimization.calc_table import minimize_sknf_calc_table, minimize_sdnf_calc_table
from utils.common import term_to_string
from utils.table_printer import print_truth_table, print_implicant_stages, print_coverage_table, print_karnaugh_map
from parser.logic_parser import VarNode, NotNode, AndNode, OrNode, ImplNode, EquivNode, tokenize, Parser, parse_expression
from truth_table.generator import generate_truth_table
from normal_forms.builder import build_sknf, build_sdnf

class TestMinimization(unittest.TestCase):
    def setUp(self):
        # Test expression 1: !(!a->!b)|c
        self.expr1 = "!(!a->!b)|c"
        self.truth_table1 = [
            {'a': 0, 'b': 0, 'c': 0, 'result': 0},
            {'a': 0, 'b': 0, 'c': 1, 'result': 1},
            {'a': 0, 'b': 1, 'c': 0, 'result': 1},
            {'a': 0, 'b': 1, 'c': 1, 'result': 1},
            {'a': 1, 'b': 0, 'c': 0, 'result': 0},
            {'a': 1, 'b': 0, 'c': 1, 'result': 1},
            {'a': 1, 'b': 1, 'c': 0, 'result': 0},
            {'a': 1, 'b': 1, 'c': 1, 'result': 1},
        ]
        self.variables1 = ['a', 'b', 'c']
        self.expected_sknf1 = "(!a | c) & (b | c)"
        self.expected_sdnf1 = "(!a & b) | (!a & c) | (a & c)"

        # Test expression 2: a & b | c
        self.expr2 = "a & b | c"
        self.truth_table2 = [
            {'a': 0, 'b': 0, 'c': 0, 'result': 0},
            {'a': 0, 'b': 0, 'c': 1, 'result': 1},
            {'a': 0, 'b': 1, 'c': 0, 'result': 0},
            {'a': 0, 'b': 1, 'c': 1, 'result': 1},
            {'a': 1, 'b': 0, 'c': 0, 'result': 0},
            {'a': 1, 'b': 0, 'c': 1, 'result': 1},
            {'a': 1, 'b': 1, 'c': 0, 'result': 1},
            {'a': 1, 'b': 1, 'c': 1, 'result': 1},
        ]
        self.variables2 = ['a', 'b', 'c']
        self.expected_sknf2 = "(a | c) & (b | c)"
        self.expected_sdnf2 = "(a & b) | c"

        # Test expression 3: !a->b
        self.expr3 = "!a->b"
        self.truth_table3 = [
            {'a': 0, 'b': 0, 'c': 0, 'result': 1},
            {'a': 0, 'b': 0, 'c': 1, 'result': 1},
            {'a': 0, 'b': 1, 'c': 0, 'result': 1},
            {'a': 0, 'b': 1, 'c': 1, 'result': 1},
            {'a': 1, 'b': 0, 'c': 0, 'result': 0},
            {'a': 1, 'b': 0, 'c': 1, 'result': 0},
            {'a': 1, 'b': 1, 'c': 0, 'result': 1},
            {'a': 1, 'b': 1, 'c': 1, 'result': 1},
        ]
        self.variables3 = ['a', 'b', 'c']
        self.expected_sknf3 = "(a | b)"
        self.expected_sdnf3 = "(!a) | (b)"

    def test_term_to_bin(self):
        term = [('a', 0), ('b', 1), ('c', None)]
        variables = ['a', 'b', 'c']
        self.assertEqual(term_to_bin(term, variables), '01_')

    def test_bin_to_term(self):
        bin_str = '01_'
        variables = ['a', 'b', 'c']
        self.assertEqual(bin_to_term(bin_str, variables), [('a', 0), ('b', 1)])

    def test_covers_minterm(self):
        implicant = [('a', 0), ('b', None), ('c', 1)]
        minterm = [('a', 0), ('b', 1), ('c', 1)]
        self.assertTrue(covers_minterm(implicant, minterm))
        minterm = [('a', 0), ('b', 1), ('c', 0)]
        self.assertFalse(covers_minterm(implicant, minterm))

    @patch('utils.table_printer.print_implicant_stages')
    def test_minimize_sknf_calculation(self, mock_print):
        result = minimize_sknf_calculation(self.truth_table1, self.variables1)
        self.assertEqual(result, self.expected_sknf1)

    @patch('utils.table_printer.print_implicant_stages')
    def test_minimize_sdnf_calculation(self, mock_print):
        result = minimize_sdnf_calculation(self.truth_table1, self.variables1)
        self.assertEqual(result, self.expected_sdnf1)

    @patch('utils.table_printer.print_implicant_stages')
    @patch('utils.table_printer.print_coverage_table')
    def test_minimize_sknf_calc_table(self, mock_coverage, mock_implicant):
        result = minimize_sknf_calc_table(self.truth_table1, self.variables1)
        self.assertEqual(result, self.expected_sknf1)

    @patch('utils.table_printer.print_implicant_stages')
    @patch('utils.table_printer.print_coverage_table')
    def test_minimize_sdnf_calc_table(self, mock_coverage, mock_implicant):
        result = minimize_sdnf_calc_table(self.truth_table1, self.variables1)
        self.assertEqual(result, self.expected_sdnf1)





    def test_generate_gray_code(self):
        self.assertEqual(generate_gray_code(1), ["0", "1"])
        self.assertEqual(generate_gray_code(2), ["00", "01", "11", "10"])
        self.assertEqual(generate_gray_code(3), ["000", "001", "011", "010", "110", "111", "101", "100"])

    def test_build_karnaugh_map(self):
        kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols = build_karnaugh_map(self.truth_table1, self.variables1)
        expected_kmap_2d = [
            [0, 1, 1, 1],
            [0, 1, 0, 1]
        ]
        self.assertEqual(kmap_2d, expected_kmap_2d)
        self.assertEqual(rows, 2)
        self.assertEqual(cols, 4)
        self.assertEqual(row_vars, ['a'])
        self.assertEqual(col_vars, ['b', 'c'])
        self.assertEqual(gray_rows, ["0", "1"])
        self.assertEqual(gray_cols, ["00", "01", "11", "10"])

    def test_find_groups(self):
        kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols = build_karnaugh_map(self.truth_table1, self.variables1)
        groups = find_groups(kmap_2d, len(self.variables1), self.variables1, rows, cols, gray_rows, gray_cols)
        self.assertTrue(len(groups) > 0)

    def test_term_to_string(self):
        term = [('a', 0), ('b', 1)]
        self.assertEqual(term_to_string(term, is_sknf=False), "!a & b")
        self.assertEqual(term_to_string(term, is_sknf=True), "a | !b")

    def test_print_truth_table(self):
        with patch('builtins.print') as mock_print:
            print_truth_table(self.truth_table1, self.variables1)
            self.assertTrue(mock_print.called)

    def test_print_implicant_stages(self):
        with patch('builtins.print') as mock_print:
            stages = [[[('a', 0), ('b', 1)]]]
            print_implicant_stages(stages, is_sknf=False)
            self.assertTrue(mock_print.called)

    def test_print_coverage_table(self):
        with patch('builtins.print') as mock_print:
            implicants = [[('a', 0), ('b', 1)]]
            minterms = [[('a', 0), ('b', 1), ('c', 1)]]
            coverage = [[1]]
            print_coverage_table(implicants, minterms, coverage, is_sknf=False)
            self.assertTrue(mock_print.called)

    def test_print_karnaugh_map(self):
        with patch('builtins.print') as mock_print:
            kmap = [0, 1, 1, 1, 0, 1, 0, 1]
            variables = ['a', 'b', 'c']
            print_karnaugh_map(kmap, variables)
            self.assertTrue(mock_print.called)

    def test_tokenize(self):
        tokens = tokenize("!(!a->!b)|c")
        self.assertEqual(tokens, [('NOT', '!'), ('LPAREN', '('), ('NOT', '!'), ('VAR', 'a'), ('IMPL', '->'), ('NOT', '!'), ('VAR', 'b'), ('RPAREN', ')'), ('OR', '|'), ('VAR', 'c')])

    def test_parser(self):
        tokens = tokenize("!(!a->!b)|c")
        parser = Parser(tokens)
        node = parser.parse()
        self.assertIsInstance(node, OrNode)

    def test_parse_expression(self):
        node, vars = parse_expression("!(!a->!b)|c")
        self.assertEqual(sorted(vars), ['a', 'b', 'c'])
        self.assertIsInstance(node, OrNode)

    def test_generate_truth_table(self):
        node, vars = parse_expression("!(!a->!b)|c")
        table = generate_truth_table(node, vars)
        self.assertEqual(len(table), 8)
        self.assertEqual(table[0]['result'], False)
        self.assertEqual(table[1]['result'], True)

    def test_build_sknf(self):
        node, vars = parse_expression("!(!a->!b)|c")
        table = generate_truth_table(node, vars)
        sknf = build_sknf(table, vars)
        self.assertEqual(sknf, "(a | b | c) & (!a | b | c) & (!a | !b | c)")

    def test_build_sdnf(self):
        node, vars = parse_expression("!(!a->!b)|c")
        table = generate_truth_table(node, vars)
        sdnf = build_sdnf(table, vars)
        self.assertEqual(sdnf, "(!a & !b & c) | (!a & b & !c) | (!a & b & c) | (a & !b & c) | (a & b & c)")

if __name__ == '__main__':
    unittest.main()