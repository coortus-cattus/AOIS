from src.binary_codes import BinaryNumber
from itertools import dropwhile

def dec_to_bin_positive(n, bits=32):
    """Перевод десятичного целого положительного числа в двоичный вид как массив бит"""
    if n == 0:
        return [0] * bits
    result = []
    while n > 0:
        result.insert(0, n % 2)
        n //= 2
    return [0] * (bits - len(result)) + result

def convert_all_tipes(num: BinaryNumber) -> None:
    num.dec_to_bin()
    num.bin_to_reverse_code()
    num.rev_code_to_compl_code()

def twos_complement_to_decimal(bits: list[int]) -> int:
    """
    Переводит 32-битное число в дополнительном коде (в виде списка из 0 и 1) в десятичное число.
    """
    result = 0
    is_negative = bits[0] == 1

    for i in range(32):
        bit = bits[31 - i]
        if is_negative:
            bit = 1 - bit
        result += bit * (1 << i)

    if is_negative:
        result = -(result + 1)

    return result

def sum_in_compl_code(num1: BinaryNumber, num2: BinaryNumber) -> list[int]:
    """Складываем 2 числа в дополнительном коде"""
    compl_1 = num1.compl_code[::-1]
    compl_2 = num2.compl_code[::-1]
    overflow = 0
    res = []
    for buff in zip(compl_1, compl_2):
        value = buff[0] + buff[1] + overflow
        overflow = value // 2
        res.append(value % 2)
    res = res[::-1]
    return res[:32]  # Ограничиваем длину до 32 бит

def subtraction(num1: BinaryNumber, num2: BinaryNumber) -> list[int]:
    """Ищет разность, отрицая отнимаемое число"""
    convert_all_tipes(num2)
    num2.negation_of_decimal_num()
    convert_all_tipes(num1)
    convert_all_tipes(num2)
    substr = sum_in_compl_code(num1, num2)
    num2.negation_of_decimal_num()
    convert_all_tipes(num2)
    return substr

def binary_to_decimal(bits: list[int]) -> int:
    """
    Переводит число в прямом двоичном коде (список из 0 и 1) в десятичное число.
    Работает с битами произвольной длины, дополняя нули слева, если нужно.
    """
    result = 0
    bits = [0] * (32 - len(bits)) + bits if len(bits) < 32 else bits[-32:]

    if bits[0] == 1:
        sign = -1
        bits = bits[:]  # Создаем копию, чтобы не менять оригинал
        bits[0] = 0
    else:
        sign = 1

    for i in range(32):
        bit = bits[31 - i]
        result += bit * (1 << i)

    return sign * result

def multiplication(num1: BinaryNumber, num2: BinaryNumber) -> list[int]:
    """Перемножает 2 числа"""
    convert_all_tipes(num1)
    convert_all_tipes(num2)
    num1_bits = num1.binary_num[::-1]
    num2_bits = num2.binary_num[::-1]
    res = [0] * 32
    for i, bit in enumerate(num2_bits):
        if bit == 1:
            shifted_num1 = [0] * i + num1_bits
            overflow = 0
            temp_res = res[:]
            for j in range(32):
                bit1 = temp_res[j] if j < len(temp_res) else 0
                bit2 = shifted_num1[j] if j < len(shifted_num1) else 0
                value = bit1 + bit2 + overflow
                res[j] = value % 2
                overflow = value // 2
    res = res[::-1]
    if (num1.sign_bit == [1] and num2.sign_bit == [0]) or (num1.sign_bit == [0] and num2.sign_bit == [1]):
        res[0] = 1
    else:
        res[0] = 0
    return res

def binary_fraction_to_decimal(binary_result: tuple) -> float:
    """
    Переводит двоичное дробное число в формате ([целая часть, None, дробная часть], знак)
    в десятичное дробное число.
    """
    binary, sign = binary_result
    if sign not in (0, 1):
        raise ValueError("Знак должен быть 0 (положительный) или 1 (отрицательный)")
    if None not in binary:
        raise ValueError("Список должен содержать None как разделитель между целой и дробной частями")
    separator_index = binary.index(None)
    integer_part = binary[:separator_index]
    fractional_part = binary[separator_index + 1:]
    if len(fractional_part) != 5:
        raise ValueError("Дробная часть должна содержать ровно 5 бит")
    integer_value = 0
    for i, bit in enumerate(integer_part):
        if bit not in (0, 1):
            raise ValueError("Целая часть должна содержать только 0 или 1")
        integer_value += bit * (2 ** (len(integer_part) - 1 - i))
    fractional_value = 0
    for i, bit in enumerate(fractional_part):
        if bit not in (0, 1):
            raise ValueError("Дробная часть должна содержать только 0 или 1")
        fractional_value += bit * (2 ** (-i - 1))
    result = integer_value + fractional_value
    return result if sign == 0 else -result

def division(num1: 'BinaryNumber', num2: 'BinaryNumber'):
    """
    Выполняет деление двух чисел в двоичной форме (BinaryNumber).
    Возвращает кортеж: (список бит [целая часть, None, дробная часть (5 бит)], знак результата)
    """
    convert_all_tipes(num1)
    convert_all_tipes(num2)
    sign1 = num1.sign_bit[0]
    sign2 = num2.sign_bit[0]
    result_sign = 0 if sign1 == sign2 else 1
    num1_abs = BinaryNumber(abs(num1.decimal_num))
    num2_abs = BinaryNumber(abs(num2.decimal_num))
    convert_all_tipes(num1_abs)
    convert_all_tipes(num2_abs)
    num2_bits = list(dropwhile(lambda x: x == 0, num2_abs.binary_num))
    if not num2_bits:
        raise ValueError("Деление на ноль невозможно")
    num1_bits = list(dropwhile(lambda x: x == 0, num1_abs.binary_num))
    if len(num1_bits) < len(num2_bits) or binary_to_decimal(num1_bits) < binary_to_decimal(num2_bits):
        result = [0]
        current = num1_bits
    else:
        current = []
        result = []
        for bit in num1_bits:
            current.append(bit)
            current = list(dropwhile(lambda x: x == 0, current))
            if binary_to_decimal(current) >= binary_to_decimal(num2_bits):
                result.append(1)
                current = dec_to_bin_positive(binary_to_decimal(current) - binary_to_decimal(num2_bits))
                current = list(dropwhile(lambda x: x == 0, current))
            else:
                result.append(0)
    result.append(None)
    for _ in range(5):
        current.append(0)
        current = list(dropwhile(lambda x: x == 0, current))
        if binary_to_decimal(current) >= binary_to_decimal(num2_bits):
            result.append(1)
            current = dec_to_bin_positive(binary_to_decimal(current) - binary_to_decimal(num2_bits))
            current = list(dropwhile(lambda x: x == 0, current))
        else:
            result.append(0)
    while len(result) > 1 and result[0] == 0 and result[1] != None:
        result.pop(0)
    return result, result_sign