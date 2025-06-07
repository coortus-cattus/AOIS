import unittest
from src.binary_codes import BinaryNumber

class TestBinaryNumber(unittest.TestCase):
    
    def test_init_positive_number(self):
        """Тестирование инициализации с положительным числом."""
        bn = BinaryNumber(42)
        self.assertEqual(bn.decimal_num, 42)
        self.assertEqual(bn.sign_bit, [0])
        self.assertEqual(bn.binary_num, [])
        self.assertEqual(bn.reverse_code, [])
        self.assertEqual(bn.compl_code, [])

    def test_init_negative_number(self):
        """Тестирование инициализации с отрицательным числом."""
        bn = BinaryNumber(-42)
        self.assertEqual(bn.decimal_num, -42)
        self.assertEqual(bn.sign_bit, [0])
        self.assertEqual(bn.binary_num, [])
        self.assertEqual(bn.reverse_code, [])
        self.assertEqual(bn.compl_code, [])

    def test_init_zero(self):
        """Тестирование инициализации с нулем."""
        bn = BinaryNumber(0)
        self.assertEqual(bn.decimal_num, 0)
        self.assertEqual(bn.sign_bit, [0])
        self.assertEqual(bn.binary_num, [])
        self.assertEqual(bn.reverse_code, [])
        self.assertEqual(bn.compl_code, [])

    def test_negation_positive_to_negative(self):
        """Тестирование инверсии с положительного на отрицательное число."""
        bn = BinaryNumber(42)
        bn.negation_of_decimal_num()
        self.assertEqual(bn.decimal_num, -42)
        self.assertEqual(bn.sign_bit, [1])
        self.assertEqual(bn.binary_num, [])
        self.assertEqual(bn.reverse_code, [])
        self.assertEqual(bn.compl_code, [])

    def test_negation_negative_to_positive(self):
        """Тестирование инверсии с отрицательного на положительное число."""
        bn = BinaryNumber(-42)
        bn.dec_to_bin()
        bn.negation_of_decimal_num()
        self.assertEqual(bn.decimal_num, 42)
        self.assertEqual(bn.sign_bit, [0])
        self.assertEqual(bn.binary_num, [])
        self.assertEqual(bn.reverse_code, [])
        self.assertEqual(bn.compl_code, [])

    def test_negation_zero(self):
        """Тестирование инверсии нуля (должен остаться нулем)."""
        bn = BinaryNumber(0)
        bn.negation_of_decimal_num()
        self.assertEqual(bn.decimal_num, 0)
        self.assertEqual(bn.sign_bit, [1])
        self.assertEqual(bn.binary_num, [])
        self.assertEqual(bn.reverse_code, [])
        self.assertEqual(bn.compl_code, [])

    def test_dec_to_bin_positive_number(self):
        """Тестирование преобразования десятичного числа в двоичное для положительного числа."""
        bn = BinaryNumber(42)
        result = bn.dec_to_bin(bits=8)
        expected = [0, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(result, expected)
        self.assertEqual(bn.binary_num, expected)
        self.assertEqual(bn.sign_bit, [0])

    def test_dec_to_bin_negative_number(self):
        """Тестирование преобразования десятичного числа в двоичное для отрицательного числа."""
        bn = BinaryNumber(-42)
        result = bn.dec_to_bin(bits=8)
        expected = [0, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(result, expected)
        self.assertEqual(bn.binary_num, expected)
        self.assertEqual(bn.sign_bit, [1])

    def test_dec_to_bin_zero(self):
        """Тестирование преобразования десятичного числа в двоичное для нуля."""
        bn = BinaryNumber(0)
        result = bn.dec_to_bin(bits=8)
        expected = [0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(result, expected)
        self.assertEqual(bn.binary_num, expected)
        self.assertEqual(bn.sign_bit, [0])

    def test_dec_to_bin_custom_bits(self):
        """Тестирование преобразования десятичного числа в двоичное с пользовательским количеством битов."""
        bn = BinaryNumber(5)
        result = bn.dec_to_bin(bits=4)
        expected = [0, 1, 0, 1]
        self.assertEqual(result, expected)
        self.assertEqual(bn.binary_num, expected)
        self.assertEqual(bn.sign_bit, [0])

    def test_bin_to_reverse_code_positive(self):
        """Тестирование преобразования двоичного числа в обратный код для положительного числа."""
        bn = BinaryNumber(42)
        bn.dec_to_bin(bits=8)
        result = bn.bin_to_reverse_code()
        expected = [0, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(result, expected)
        self.assertEqual(bn.reverse_code, expected)

    def test_bin_to_reverse_code_negative(self):
        """Тестирование преобразования двоичного числа в обратный код для отрицательного числа."""
        bn = BinaryNumber(-42)
        bn.dec_to_bin(bits=8)
        result = bn.bin_to_reverse_code()
        expected = [1, 1, 0, 1, 0, 1, 0, 1]
        self.assertEqual(result, expected)
        self.assertEqual(bn.reverse_code, expected)

    def test_bin_to_reverse_code_zero(self):
        """Тестирование преобразования двоичного числа в обратный код для нуля."""
        bn = BinaryNumber(0)
        bn.dec_to_bin(bits=8)
        result = bn.bin_to_reverse_code()
        expected = [0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(result, expected)
        self.assertEqual(bn.reverse_code, expected)

    def test_rev_code_to_compl_code_positive(self):
        """Тестирование преобразования обратного кода в дополнительный для положительного числа."""
        bn = BinaryNumber(42)
        bn.dec_to_bin(bits=8)
        bn.bin_to_reverse_code()
        result = bn.rev_code_to_compl_code()
        expected = [0, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(result, expected)
        self.assertEqual(bn.compl_code, expected)

    def test_rev_code_to_compl_code_negative(self):
        """Тестирование преобразования обратного кода в дополнительный для отрицательного числа."""
        bn = BinaryNumber(-42)
        bn.dec_to_bin(bits=8)
        bn.bin_to_reverse_code()
        result = bn.rev_code_to_compl_code()
        expected = [1, 1, 0, 1, 0, 1, 1, 0]
        self.assertEqual(result, expected)
        self.assertEqual(bn.compl_code, expected)

    def test_rev_code_to_compl_code_zero(self):
        """Тестирование преобразования обратного кода в дополнительный для нуля."""
        bn = BinaryNumber(0)
        bn.dec_to_bin(bits=8)
        bn.bin_to_reverse_code()
        result = bn.rev_code_to_compl_code()
        expected = [0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(result, expected)
        self.assertEqual(bn.compl_code, expected)

    def test_properties_immutability(self):
        """Тестирование невозможности изменения свойств напрямую."""
        bn = BinaryNumber(42)
        with self.assertRaises(AttributeError):
            bn.decimal_num = 100
        with self.assertRaises(AttributeError):
            bn.sign_bit = [1]
        with self.assertRaises(AttributeError):
            bn.binary_num = [1, 0]
        with self.assertRaises(AttributeError):
            bn.reverse_code = [1, 0]
        with self.assertRaises(AttributeError):
            bn.compl_code = [1, 0]

if __name__ == '__main__':
    unittest.main()