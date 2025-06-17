import unittest
from src.ieee754 import IEEE754Float, add_ieee754

class TestIEEE754(unittest.TestCase):
    
    def test_init(self):
        """Тестирование инициализации IEEE754Float."""
        num = IEEE754Float(0, 127, [0] * 23)
        self.assertEqual(num.sign, 0)
        self.assertEqual(num.exponent, 127)
        self.assertEqual(num.mantissa, [0] * 23)
        
        # Проверка обрезки мантиссы до 23 бит
        long_mantissa = [1] * 25
        num = IEEE754Float(0, 128, long_mantissa)
        self.assertEqual(num.mantissa, [1] * 23)

    def test_from_decimal_zero(self):
        """Тестирование преобразования нуля в IEEE-754."""
        num = IEEE754Float.from_decimal(0.0)
        self.assertEqual(num.sign, 0)
        self.assertEqual(num.exponent, 0)
        self.assertEqual(num.mantissa, [0] * 23)

    def test_from_decimal_positive_integer(self):
        """Тестирование преобразования положительного целого числа."""
        num = IEEE754Float.from_decimal(2.0)
        self.assertEqual(num.sign, 0)
        self.assertEqual(num.exponent, 128)  # 127 + 1 (2 = 1.0 * 2^1)
        self.assertEqual(num.mantissa, [0] * 23)  # 1.0 -> мантисса 0 (неявная 1)

    def test_from_decimal_positive_fraction(self):
        """Тестирование преобразования положительного дробного числа."""
        num = IEEE754Float.from_decimal(0.5)
        self.assertEqual(num.sign, 0)
        self.assertEqual(num.exponent, 126)  # 127 - 1 (0.5 = 1.0 * 2^-1)
        self.assertEqual(num.mantissa, [0] * 23)  # 1.0 -> мантисса 0

    def test_from_decimal_exceptions(self):
        """Тестирование исключений в from_decimal."""
        with self.assertRaises(ValueError):
            IEEE754Float.from_decimal(-1.0)  # Отрицательное число


    def test_to_decimal_zero(self):
        """Тестирование преобразования нуля из IEEE-754 в десятичное."""
        num = IEEE754Float(0, 0, [0] * 23)
        self.assertEqual(num.to_decimal(), 0.0)

    def test_to_decimal_positive_integer(self):
        """Тестирование преобразования целого числа из IEEE-754."""
        num = IEEE754Float(0, 128, [0] * 23)  # 2.0
        self.assertEqual(num.to_decimal(), 2.0)

    def test_to_decimal_positive_fraction(self):
        """Тестирование преобразования дробного числа из IEEE-754."""
        num = IEEE754Float(0, 126, [0] * 23)  # 0.5
        self.assertAlmostEqual(num.to_decimal(), 0.5)

    def test_to_bits(self):
        """Тестирование получения битового представления."""
        num = IEEE754Float(0, 128, [0] * 23)  # 2.0
        expected = [0] + [1, 0, 0, 0, 0, 0, 0, 0] + [0] * 23
        self.assertEqual(num.to_bits(), expected)
        
        num = IEEE754Float(0, 126, [1] + [0] * 22)  # 0.75
        expected = [0] + [0, 1, 1, 1, 1, 1, 1, 0] + [1] + [0] * 22
        self.assertEqual(num.to_bits(), expected)

    def test_add_ieee754_zero(self):
        """Тестирование сложения с нулем."""
        num1 = IEEE754Float(0, 0, [0] * 23)  # 0.0
        num2 = IEEE754Float(0, 128, [0] * 23)  # 2.0
        result = add_ieee754(num1, num2)
        self.assertEqual(result.sign, 0)
        self.assertEqual(result.exponent, 128)
        self.assertEqual(result.mantissa, [0] * 23)

    def test_add_ieee754_same_exponent(self):
        """Тестирование сложения чисел с одинаковой экспонентой."""
        num1 = IEEE754Float(0, 128, [0] * 23)  # 2.0
        num2 = IEEE754Float(0, 128, [0] * 23)  # 2.0
        result = add_ieee754(num1, num2)
        self.assertEqual(result.sign, 0)
        self.assertEqual(result.exponent, 129)  # 4.0 = 1.0 * 2^2
        self.assertEqual(result.mantissa, [0] * 23)

    def test_add_ieee754_different_exponents(self):
        """Тестирование сложения чисел с разными экспонентами."""
        num1 = IEEE754Float(0, 128, [0] * 23)  # 2.0
        num2 = IEEE754Float(0, 126, [0] * 23)  # 0.5
        result = add_ieee754(num1, num2)
        self.assertEqual(result.sign, 0)
        self.assertEqual(result.exponent, 128)  # 2.5 = 1.25 * 2^1
        expected_mantissa = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 0.25
        self.assertEqual(result.mantissa[:2], expected_mantissa[:2])

    def test_add_ieee754_exceptions(self):
        """Тестирование исключений при сложении."""
        num1 = IEEE754Float(0, 254, [0] * 23)  # Большое число
        num2 = IEEE754Float(0, 254, [0] * 23)  # Большое число
        with self.assertRaises(ValueError):
            add_ieee754(num1, num2)  # Переполнение экспоненты

if __name__ == '__main__':
    unittest.main()