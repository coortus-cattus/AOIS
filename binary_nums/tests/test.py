import unittest

import src.binary_codes as binary_codes

def convert_all_tipes(num: binary_codes.BinaryNumber):
    num.dec_to_bin()
    num.bin_to_reverse_code()
    num.rev_code_to_compl_code()

class TestBinaryCodes(unittest.TestCase):
    
    def setUp(self):
        self.binary_num1 = binary_codes.BinaryNumber(5)
        self.binary_num2 = binary_codes.BinaryNumber(-5)
        self.binary_num3 = binary_codes.BinaryNumber(0)
        self.bn = binary_codes.BinaryNumber(0)
    
    def test_dec_to_bin(self):
        num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
        num2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.assertEqual(self.binary_num1.dec_to_bin(), num)
        self.assertEqual(self.binary_num1.sign_bit, [0])

        self.assertEqual(self.binary_num2.dec_to_bin(), num)
        self.assertEqual(self.binary_num2.sign_bit, [1])

        self.assertEqual(self.binary_num3.dec_to_bin(), num2)
        self.assertEqual(self.binary_num3.sign_bit, [0])

    def test_bin_to_reverse_code(self):
        num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
        num2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0]
        
        convert_all_tipes(self.binary_num1)
        convert_all_tipes(self.binary_num2)

        self.assertEqual(self.binary_num1.bin_to_reverse_code(), num)
        self.assertEqual(self.binary_num2.bin_to_reverse_code(), num2)

    def test_rev_code_to_compl_code(self):
        num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
        num2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]

        convert_all_tipes(self.binary_num1)
        convert_all_tipes(self.binary_num2)

        self.assertEqual(self.binary_num1.rev_code_to_compl_code(), num)
        self.assertEqual(self.binary_num2.rev_code_to_compl_code(), num2)

    def test_negation_of_decimal_num(self):
        self.binary_num1.dec_to_bin()
        self.binary_num2.dec_to_bin()

        self.binary_num1.negation_of_decimal_num()
        self.binary_num2.negation_of_decimal_num()

        self.assertEqual(self.binary_num1.decimal_num, -5)
        self.assertEqual(self.binary_num1.sign_bit, [1])
        self.assertEqual(self.binary_num1.binary_num, [])
        self.assertEqual(self.binary_num1.reverse_code, [])
        self.assertEqual(self.binary_num1.compl_code, [])

        self.assertEqual(self.binary_num2.decimal_num, 5)
        self.assertEqual(self.binary_num2.sign_bit, [0])
        

if __name__ == '__main__':
    unittest.main()

