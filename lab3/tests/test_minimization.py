import unittest
from unittest.mock import patch, MagicMock
from minimization.calculation import term_to_bin, bin_to_term, covers_minterm, minimize_sknf_calculation, minimize_sdnf_calculation
from minimization.karnaugh import generate_gray_code, build_karnaugh_map, find_maximal_rectangles, find_essential_groups, group_to_term, minimize_sknf_karnaugh, minimize_sdnf_karnaugh
from minimization.calc_table import minimize_sknf_calc_table, minimize_sdnf_calc_table
from utils.common import term_to_string
from utils.table_printer import print_truth_table, print_implicant_stages, print_coverage_table, print_karnaugh_map
from parser.logic_parser import tokenize, Parser, parse_expression
from truth_table.generator import generate_truth_table
from normal_forms.builder import build_sknf, build_sdnf

class TestMinimization(unittest.TestCase):
    def setUp(self):
        # Test expression 1: !(!a->!b)|c
        self.expr1 = "!(!a->!b)|c"
        self.root1, self.variables1 = parse_expression(self.expr1)
        self.truth_table1 = generate_truth_table(self.root1, self.variables1)
        
        # Test expression 2: a & b | c
        self.expr2 = "a & b | c"
        self.root2, self.variables2 = parse_expression(self.expr2)
        self.truth_table2 = generate_truth_table(self.root2, self.variables2)
        
        # Test expression 3: !a->b
        self.expr3 = "!a->b"
        self.root3, self.variables3 = parse_expression(self.expr3)
        self.truth_table3 = generate_truth_table(self.root3, self.variables3)

    # Calculation method tests
    @patch('minimization.calculation.print_implicant_stages')
    def test_minimize_sknf_calculation_basic(self, mock_print):
        result = minimize_sknf_calculation(self.truth_table1, self.variables1)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    @patch('minimization.calculation.print_implicant_stages')
    def test_minimize_sdnf_calculation_basic(self, mock_print):
        result = minimize_sdnf_calculation(self.truth_table1, self.variables1)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    @patch('minimization.calculation.print_implicant_stages')
    def test_minimize_sknf_calculation_empty(self, mock_print):
        empty_table = [{'a': 0, 'b': 0, 'c': 0, 'result': True} for _ in range(8)]
        result = minimize_sknf_calculation(empty_table, self.variables1)
        self.assertEqual(result, "1")

    @patch('minimization.calculation.print_implicant_stages')
    def test_minimize_sdnf_calculation_empty(self, mock_print):
        empty_table = [{'a': 0, 'b': 0, 'c': 0, 'result': False} for _ in range(8)]
        result = minimize_sdnf_calculation(empty_table, self.variables1)
        self.assertEqual(result, "0")

    # Table method tests
    @patch('minimization.calc_table.print_implicant_stages')
    @patch('minimization.calc_table.print_coverage_table')
    def test_minimize_sknf_calc_table_basic(self, mock_coverage, mock_implicant):
        result = minimize_sknf_calc_table(self.truth_table1, self.variables1)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    @patch('minimization.calc_table.print_implicant_stages')
    @patch('minimization.calc_table.print_coverage_table')
    def test_minimize_sdnf_calc_table_basic(self, mock_coverage, mock_implicant):
        result = minimize_sdnf_calc_table(self.truth_table1, self.variables1)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    # Karnaugh method tests
    def test_generate_gray_code(self):
        self.assertEqual(generate_gray_code(0), [""])
        self.assertEqual(generate_gray_code(1), ["0", "1"])
        self.assertEqual(generate_gray_code(2), ["00", "01", "11", "10"])
        self.assertEqual(generate_gray_code(3), ["000", "001", "011", "010", "110", "111", "101", "100"])

    def test_build_karnaugh_map_basic(self):
        result = build_karnaugh_map(self.truth_table1, self.variables1)
        self.assertIsNotNone(result)
        kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols = result
        self.assertEqual(rows, 2)
        self.assertEqual(cols, 4)
        self.assertEqual(row_vars, ['a'])
        self.assertEqual(col_vars, ['b', 'c'])

    def test_build_karnaugh_map_sknf(self):
        result = build_karnaugh_map(self.truth_table1, self.variables1, is_sknf=True)
        self.assertIsNotNone(result)

    def test_build_karnaugh_map_too_many_vars(self):
        many_vars = ['a', 'b', 'c', 'd', 'e', 'f']
        result = build_karnaugh_map(self.truth_table1, many_vars)
        self.assertIsNone(result[0])

    def test_find_maximal_rectangles(self):
        kmap_2d = [
            [1, 0, 1, 0],
            [0, 1, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0]
        ]
        groups = find_maximal_rectangles(kmap_2d, target=1)
        self.assertIsInstance(groups, list)
        self.assertTrue(len(groups) > 0)

    def test_find_maximal_rectangles_no_target(self):
        kmap_2d = [[0, 0], [0, 0]]
        groups = find_maximal_rectangles(kmap_2d, target=1)
        self.assertEqual(groups, [])

    def test_find_essential_groups(self):
        kmap_2d = [[1, 0], [0, 1]]
        groups = find_essential_groups(kmap_2d, target=1)
        self.assertIsInstance(groups, list)

    def test_find_essential_groups_no_target(self):
        kmap_2d = [[0, 0], [0, 0]]
        groups = find_essential_groups(kmap_2d, target=1)
        self.assertEqual(groups, [])

    def test_group_to_term(self):
        group = {(0, 0), (0, 1)}
        row_vars, col_vars = ['a'], ['b']
        gray_rows, gray_cols = ['0', '1'], ['00', '01', '11', '10']
        term = group_to_term(group, row_vars, col_vars, gray_rows, gray_cols, is_sknf=False)
        self.assertIsInstance(term, list)

    def test_group_to_term_empty(self):
        term = group_to_term(set(), [], [], [], [], False)
        self.assertEqual(term, [])

    @patch('utils.table_printer.print_karnaugh_map')
    def test_minimize_sknf_karnaugh_basic(self, mock_print):
        result = minimize_sknf_karnaugh(self.truth_table1, self.variables1)
        self.assertIsInstance(result, str)

    @patch('utils.table_printer.print_karnaugh_map')
    def test_minimize_sdnf_karnaugh_basic(self, mock_print):
        result = minimize_sdnf_karnaugh(self.truth_table1, self.variables1)
        self.assertIsInstance(result, str)

    @patch('utils.table_printer.print_karnaugh_map')
    def test_minimize_sknf_karnaugh_too_many_vars(self, mock_print):
        many_vars = ['a', 'b', 'c', 'd', 'e', 'f']
        result = minimize_sknf_karnaugh(self.truth_table1, many_vars)
        self.assertEqual(result, "1")

    @patch('utils.table_printer.print_karnaugh_map')
    def test_minimize_sdnf_karnaugh_too_many_vars(self, mock_print):
        many_vars = ['a', 'b', 'c', 'd', 'e', 'f']
        result = minimize_sdnf_karnaugh(self.truth_table1, many_vars)
        self.assertEqual(result, "0")

    # Utility function tests
    def test_term_to_bin(self):
        term = [('a', 0), ('b', 1), ('c', None)]
        variables = ['a', 'b', 'c']
        self.assertEqual(term_to_bin(term, variables), '01_')

    def test_bin_to_term(self):
        bin_str = '01_'
        variables = ['a', 'b', 'c']
        result = bin_to_term(bin_str, variables)
        self.assertEqual(result, [('a', 0), ('b', 1)])

    def test_covers_minterm(self):
        implicant = [('a', 0), ('b', None), ('c', 1)]
        minterm = [('a', 0), ('b', 1), ('c', 1)]
        self.assertTrue(covers_minterm(implicant, minterm))

        minterm2 = [('a', 0), ('b', 1), ('c', 0)]
        self.assertFalse(covers_minterm(implicant, minterm2))

    def test_term_to_string(self):
        term = [('a', 0), ('b', 1)]
        self.assertEqual(term_to_string(term, is_sknf=False), "!a & b")
        self.assertEqual(term_to_string(term, is_sknf=True), "a | !b")

    def test_term_to_string_empty(self):
        self.assertEqual(term_to_string([], False), "0")
        self.assertEqual(term_to_string([], True), "1")

    # Parser and table generation tests
    def test_tokenize(self):
        tokens = tokenize("!(!a->!b)|c")
        expected = [
            ('NOT', '!'), ('LPAREN', '('), ('NOT', '!'), ('VAR', 'a'),
            ('IMPL', '->'), ('NOT', '!'), ('VAR', 'b'), ('RPAREN', ')'),
            ('OR', '|'), ('VAR', 'c')
        ]
        self.assertEqual(tokens, expected)

    def test_parser(self):
        tokens = tokenize("a & b")
        parser = Parser(tokens)
        node = parser.parse()
        self.assertIsNotNone(node)

    def test_parse_expression(self):
        node, variables = parse_expression("a & b | c")
        self.assertIsNotNone(node)
        self.assertEqual(sorted(variables), ['a', 'b', 'c'])

    def test_generate_truth_table(self):
        table = generate_truth_table(self.root1, self.variables1)
        self.assertEqual(len(table), 8)
        self.assertIn('result', table[0])

    def test_build_sknf(self):
        sknf = build_sknf(self.truth_table1, self.variables1)
        self.assertIsInstance(sknf, str)
        self.assertTrue(len(sknf) > 0)

    def test_build_sdnf(self):
        sdnf = build_sdnf(self.truth_table1, self.variables1)
        self.assertIsInstance(sdnf, str)
        self.assertTrue(len(sdnf) > 0)

    # Mock tests for printer functions
    def test_print_functions(self):
        with patch('builtins.print') as mock_print:
            # Test truth table printing
            print_truth_table(self.truth_table1, self.variables1)
            self.assertTrue(mock_print.called)
            
            mock_print.reset_mock()
            
            # Test implicant stages printing
            stages = [[[('a', 0), ('b', 1)]]]
            print_implicant_stages(stages)
            self.assertTrue(mock_print.called)
            
            mock_print.reset_mock()
            
            # Test coverage table printing
            implicants = [[('a', 0), ('b', 1)]]
            minterms = [[('a', 0), ('b', 1), ('c', 1)]]
            coverage = [[1]]
            print_coverage_table(implicants, minterms, coverage)
            self.assertTrue(mock_print.called)
            
            mock_print.reset_mock()
            
            # Test karnaugh map printing
            kmap = [0, 1, 1, 1, 0, 1, 0, 1]
            variables = ['a', 'b', 'c']
            print_karnaugh_map(kmap, variables)
            self.assertTrue(mock_print.called)

    # Edge case tests
    def test_edge_cases(self):


        # Test with always true function
        always_true = [{'a': 0, 'b': 0, 'result': True}, {'a': 0, 'b': 1, 'result': True},
                      {'a': 1, 'b': 0, 'result': True}, {'a': 1, 'b': 1, 'result': True}]
        result = minimize_sdnf_karnaugh(always_true, ['a', 'b'])
        self.assertEqual(result, "0")  # Should be empty sum

        # Test with always false function  
        always_false = [{'a': 0, 'b': 0, 'result': False}, {'a': 0, 'b': 1, 'result': False},
                       {'a': 1, 'b': 0, 'result': False}, {'a': 1, 'b': 1, 'result': False}]
        result = minimize_sknf_karnaugh(always_false, ['a', 'b'])
        self.assertEqual(result, "1")  # Should be empty product

if __name__ == '__main__':
    unittest.main()