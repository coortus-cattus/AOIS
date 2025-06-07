# ieee754.py
import math

class IEEE754Float:
    def __init__(self, sign: int, exponent: int, mantissa: list):
        """
        Инициализация числа в формате IEEE-754 (32 бита).
        """
        self.sign = sign
        self.exponent = exponent
        self.mantissa = mantissa[:23]  # Ограничиваем до 23 бит
    
    @staticmethod
    def from_decimal(decimal: float) -> 'IEEE754Float':
        """
        Преобразует десятичное число в формат IEEE-754 (32 бита).
        """
        if decimal < 0:
            raise ValueError("Ожидается положительное число")
        if decimal == 0:
            return IEEE754Float(0, 0, [0] * 23)
        
        int_part = int(decimal)
        frac_part = decimal - int_part
        
        if int_part == 0:
            int_bits = []
        else:
            int_bits = []
            while int_part > 0:
                int_bits.insert(0, int_part % 2)
                int_part //= 2
        
        frac_bits = []
        precision = 23
        while frac_part > 0 and len(frac_bits) < precision:
            frac_part *= 2
            bit = int(frac_part)
            frac_bits.append(bit)
            frac_part -= bit
        
        bits = int_bits + frac_bits
        
        exponent = 0
        if bits and bits[0] == 1:
            exponent = len(int_bits) - 1
            mantissa = bits[1:]
        else:
            for i, bit in enumerate(bits):
                if bit == 1:
                    exponent = -(i + 1)
                    mantissa = bits[i + 1:]
                    break
            else:
                return IEEE754Float(0, 0, [0] * 23)
        
        mantissa = mantissa + [0] * (23 - len(mantissa)) if len(mantissa) < 23 else mantissa[:23]
        exponent += 127
        
        if exponent > 255:
            raise ValueError("Число слишком большое для IEEE-754 (32 бита)")
        if exponent < 0:
            return IEEE754Float(0, 0, [0] * 23)
        
        return IEEE754Float(0, exponent, mantissa)
    
    def to_decimal(self) -> float:
        """
        Преобразует число в формате IEEE-754 обратно в десятичное.
        """
        if self.exponent == 0 and all(bit == 0 for bit in self.mantissa):
            return 0.0
        
        true_exponent = self.exponent - 127
        mantissa_value = 1.0
        for i, bit in enumerate(self.mantissa):
            mantissa_value += bit * (2 ** -(i + 1))
        
        return mantissa_value * (2 ** true_exponent)
    
    def to_bits(self) -> list:
        """
        Возвращает 32-битное представление числа в виде списка бит.
        """
        bits = [self.sign]
        exp_bits = []
        exp = self.exponent
        for _ in range(8):
            exp_bits.insert(0, exp % 2)
            exp //= 2
        bits.extend(exp_bits)
        bits.extend(self.mantissa)
        return bits

def add_ieee754(num1: IEEE754Float, num2: IEEE754Float) -> IEEE754Float:
    """
    Складывает два числа в формате IEEE-754 (32 бита).
    """
    # Проверяем нули
    if num1.exponent == 0 and all(bit == 0 for bit in num1.mantissa):
        return num2
    if num2.exponent == 0 and all(bit == 0 for bit in num2.mantissa):
        return num1

    # Получаем истинные мантиссы (неявная 1 впереди)
    mant1 = [1] + num1.mantissa
    mant2 = [1] + num2.mantissa

    exp1 = num1.exponent
    exp2 = num2.exponent

    # Выравниваем экспоненты
    if exp1 > exp2:
        shift = exp1 - exp2
        for _ in range(shift):
            mant2 = [0] + mant2[:-1]  # сдвиг вправо
        exp = exp1
    else:
        shift = exp2 - exp1
        for _ in range(shift):
            mant1 = [0] + mant1[:-1]  # сдвиг вправо
        exp = exp2

    # Сложение мантисс
    carry = 0
    result_mant = []
    for i in range(len(mant1) - 1, -1, -1):
        bit_sum = mant1[i] + mant2[i] + carry
        result_mant.insert(0, bit_sum % 2)
        carry = bit_sum // 2

    if carry:
        result_mant = [1] + result_mant
        exp += 1

    # Нормализация: ищем первую 1
    shift = 0
    for i, bit in enumerate(result_mant):
        if bit == 1:
            break
        shift += 1

    exp -= shift
    result_mant = result_mant[shift:]

    # Убираем неявную 1
    if len(result_mant) > 1:
        result_mant = result_mant[1:]
    else:
        result_mant = [0] * 23

    # Дополняем или обрезаем мантиссу
    result_mant = result_mant + [0] * (23 - len(result_mant)) if len(result_mant) < 23 else result_mant[:23]

    if exp <= 0:
        return IEEE754Float(0, 0, [0] * 23)
    if exp >= 255:
        raise ValueError("Переполнение экспоненты")

    return IEEE754Float(0, exp, result_mant)
