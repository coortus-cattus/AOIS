import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from matrix import Matrix
from arithmetic import extract_fields, add_fields
from logical_ops import apply_logical_function
from search import find_words_by_V

class TestMatrixOperations(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовой матрицы 4x4 с диагональной адресацией"""
        self.matrix = Matrix(random_fill=False)
        self.matrix.matrix = [
            [1, 0, 1, 0],  # Строка 0
            [0, 1, 0, 1],  # Строка 1
            [1, 0, 1, 0],  # Строка 2
            [0, 1, 0, 1]   # Строка 3
        ]
        self.matrix.size = 4

    def test_get_word(self):
        """Тестирование получения слова с диагональной адресацией"""
        # Для word 0: берем элементы (0,0), (1,1), (2,2), (3,3)
        self.assertEqual(self.matrix.get_word(0), [1, 1, 1, 1])
        
        # Для word 1: берем элементы (0,1), (1,2), (2,3), (3,0)
        self.assertEqual(self.matrix.get_word(1), [0, 0, 0, 0])
        
        # Для word 2: берем элементы (0,2), (1,3), (2,0), (3,1)
        self.assertEqual(self.matrix.get_word(2), [1, 1, 1, 1])

class TestArithmeticFunctions(unittest.TestCase):
    def test_extract_fields(self):
        word = [1, 0, 1, 0, 1, 1, 0, 0]
        V, A, B = extract_fields(word, v_bits=2, a_bits=3, b_bits=3)
        self.assertEqual(V, [1, 0])
        self.assertEqual(A, [1, 0, 1])
        self.assertEqual(B, [1, 0, 0])

    def test_add_fields(self):
        self.assertEqual(add_fields([1, 0], [0, 1]), 3)  # 2 + 1 = 3

class TestLogicalFunctions(unittest.TestCase):
    def test_logical_operations(self):
        self.assertEqual(apply_logical_function("f1", [1, 0], [1, 1]), [1, 0])  # AND
        self.assertEqual(apply_logical_function("f14", [1, 0], [0, 1]), [0, 0])  # NOR

if __name__ == "__main__":
    unittest.main()