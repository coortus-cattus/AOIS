import unittest
from src.binary_codes import BinaryNumber
from src.utils import (
    dec_to_bin_positive,
    convert_all_tipes,
    twos_complement_to_decimal,
    sum_in_compl_code,
    subtraction,
    binary_to_decimal,
    multiplication,
    binary_fraction_to_decimal,
    division
)

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        self.bn_positive = BinaryNumber(42)
        self.bn_negative = BinaryNumber(-42)
        self.bn_zero = BinaryNumber(0)
        self.bn_small = BinaryNumber(5)
        self.bn_small_negative = BinaryNumber(-5)

    def test_dec_to_bin_positive(self):
        self.assertEqual(dec_to_bin_positive(42, bits=8), [0, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(dec_to_bin_positive(0, bits=8), [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(dec_to_bin_positive(5, bits=4), [0, 1, 0, 1])
        self.assertEqual(dec_to_bin_positive(255, bits=8), [1, 1, 1, 1, 1, 1, 1, 1])

    def test_convert_all_tipes(self):
        bn = BinaryNumber(42)
        convert_all_tipes(bn)
        self.assertEqual(bn.binary_num, [0] * 24 + [0, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(bn.reverse_code, [0] * 24 + [0, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(bn.compl_code, [0] * 24 + [0, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(bn.sign_bit, [0])

        bn_neg = BinaryNumber(-42)
        convert_all_tipes(bn_neg)
        self.assertEqual(bn_neg.binary_num, [0] * 24 + [0, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(bn_neg.reverse_code, [1] * 24 + [1, 1, 0, 1, 0, 1, 0, 1])
        self.assertEqual(bn_neg.compl_code, [1] * 24 + [1, 1, 0, 1, 0, 1, 1, 0])
        self.assertEqual(bn_neg.sign_bit, [1])

    def test_twos_complement_to_decimal(self):
        compl_code = [0] * 24 + [0, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(twos_complement_to_decimal(compl_code), 42)
        compl_code_neg = [1] * 24 + [1, 1, 0, 1, 0, 1, 1, 0]
        self.assertEqual(twos_complement_to_decimal(compl_code_neg), -42)
        self.assertEqual(twos_complement_to_decimal([0] * 32), 0)

    def test_multiplication(self):
        result = multiplication(self.bn_small, self.bn_small)
        self.assertEqual(result, [0] * 27 + [1, 1, 0, 0, 1])
        result = multiplication(self.bn_small, self.bn_small_negative)
        self.assertEqual(result, [1] + [0] * 26 + [1, 1, 0, 0, 1])
        result = multiplication(self.bn_zero, self.bn_positive)
        self.assertEqual(result, [0] * 32)

    def test_binary_fraction_to_decimal(self):
        self.assertEqual(binary_fraction_to_decimal(([1, 0, 1, None, 1, 0, 0, 0, 0], 0)), 5.5)
        self.assertEqual(binary_fraction_to_decimal(([1, 0, 1, None, 1, 0, 0, 0, 0], 1)), -5.5)
        self.assertEqual(binary_fraction_to_decimal(([0, None, 0, 0, 0, 0, 0], 0)), 0.0)
        with self.assertRaises(ValueError):
            binary_fraction_to_decimal(([1, 0, 1], 0))
        with self.assertRaises(ValueError):
            binary_fraction_to_decimal(([1, 0, 1, None, 1], 0))
        with self.assertRaises(ValueError):
            binary_fraction_to_decimal(([1, 2, None, 1, 0, 0, 0, 0], 0))
        with self.assertRaises(ValueError):
            binary_fraction_to_decimal(([1, 0, None, 1, 0, 0, 0, 0], 2))

    def test_division(self):
        bn_divisor = BinaryNumber(2)
        result, sign = division(self.bn_positive, bn_divisor)
        self.assertEqual(result[:result.index(None)], [1, 0, 1, 0, 1])
        self.assertEqual(sign, 0)
        result, sign = division(self.bn_negative, bn_divisor)
        self.assertEqual(result[:result.index(None)], [1, 0, 1, 0, 1])
        self.assertEqual(sign, 1)
        result, sign = division(self.bn_small, bn_divisor)
        self.assertEqual(result, [1, 0, None, 1, 0, 0, 0, 0])
        self.assertEqual(sign, 0)
        with self.assertRaises(ValueError):
            division(self.bn_positive, self.bn_zero)

if __name__ == '__main__':
    unittest.main()