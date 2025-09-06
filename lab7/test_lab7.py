import unittest
import io
from unittest.mock import patch

from arithmetic import extract_fields, add_fields, print_words_info
from logical_ops import apply_logical_function, print_logic_table
from matrix import Matrix
from search import find_words_by_V, print_search_results


class TestArithmetic(unittest.TestCase):
    def test_extract_fields_default(self):
        word = [1,0,1, 1,1,0,0, 0,1,1,0]
        V, A, B = extract_fields(word)
        self.assertEqual(V, [1,0,1])
        self.assertEqual(A, [1,1,0,0])
        self.assertEqual(B, [0,1,1,0])

    def test_add_fields(self):
        A = [1,0,1]  # 5
        B = [1,1,0]  # 6
        self.assertEqual(add_fields(A, B), 11)

    def test_print_words_info(self):
        m = Matrix(random_fill=False)
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            print_words_info(m)
            output = fake_out.getvalue()
        self.assertIn("Слова (V, A, B)", output)


class TestLogicalOps(unittest.TestCase):
    def test_apply_logical_function(self):
        cases = [
            ("f1", 1, 1, 1),
            ("f1", 1, 0, 0),
            ("f14", 0, 0, 1),
            ("f3", 1, 0, 1),
            ("f3", 1, 1, 0),
            ("f12", 1, 0, 0),
            ("f12", 0, 1, 1),
        ]
        for func, a, b, expected in cases:
            result = apply_logical_function(func, [a], [b])
            self.assertEqual(result, [expected])

    def test_print_logic_table(self):
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            print_logic_table()
            output = fake_out.getvalue()
        self.assertIn("x1 x2 | f1 f14 f3 f12", output)


class TestMatrix(unittest.TestCase):
    def test_matrix_init(self):
        m1 = Matrix(random_fill=True)
        m2 = Matrix(random_fill=False)
        self.assertEqual(len(m1.matrix), 16)
        self.assertTrue(all(val in [0,1] for row in m1.matrix for val in row))
        self.assertTrue(all(val == 0 for row in m2.matrix for val in row))

    def test_get_and_set_word(self):
        m = Matrix(random_fill=False)
        word = [1]*16
        m.set_word(0, word)
        self.assertEqual(m.get_word(0), word)

    def test_get_column(self):
        m = Matrix(random_fill=False)
        m.matrix[0][0] = 1
        col = m.get_column(0)
        self.assertEqual(len(col), 16)
        self.assertEqual(col[0], 1)

    def test_print_matrix(self):
        m = Matrix(random_fill=False)
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            m.print_matrix()
            output = fake_out.getvalue()
        self.assertIn("0", output)


class TestSearch(unittest.TestCase):
    def test_find_words_by_V_top_bottom(self):
        m = Matrix(random_fill=False)
        word = [1,0,1] + [0]*13
        m.set_word(0, word)
        top = find_words_by_V(m, [1,0,1], "top")
        bottom = find_words_by_V(m, [1,0,1], "bottom")
        self.assertEqual(top, [0])
        self.assertEqual(bottom, [0])

    def test_find_words_by_V_not_found(self):
        m = Matrix(random_fill=False)
        self.assertEqual(find_words_by_V(m, [1,1,1], "top"), [])

    def test_print_search_results(self):
        m = Matrix(random_fill=False)
        word = [1,0,1] + [0]*13
        m.set_word(0, word)
        with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
            print_search_results(m, [1,0,1])
            output = fake_out.getvalue()
        self.assertIn("Найдено сверху", output)
        self.assertIn("Найдено снизу", output)


if __name__ == "__main__":
    unittest.main()
