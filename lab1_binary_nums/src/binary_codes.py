class BinaryNumber:

    def __init__(self, decimal_num: int) -> None:
        self._decimal_num = decimal_num
        self._sign_bit: list[int] = [0]
        self._binary_num: list[int] = [] # прямой код
        self._reverse_code: list[int] = [] # обратный код
        self._compl_code: list[int] = [] # дополнительный код


    @property
    def decimal_num(self) -> int:
        return self._decimal_num

    @property
    def sign_bit(self) -> list[int]:
        return self._sign_bit
    
    @property
    def binary_num(self) -> list[int]:
        return self._binary_num
    
    @property
    def reverse_code(self) -> list[int]:
        return self._reverse_code
    
    @property
    def compl_code(self) -> list[int]:
        return self._compl_code
    
    def negation_of_decimal_num(self):
        """Меняет знак числа на противоположный"""
        self._decimal_num = -self._decimal_num
        if self._sign_bit == [0]:
            self._sign_bit = [1]
        elif self._sign_bit == [1]:
            self._sign_bit = [0]

        self._binary_num = []
        self._reverse_code = []
        self._compl_code = []

    def dec_to_bin(self, bits = 32) -> list[int]:
        """Перевод десятичного целого числа в двоичный вид как массив бит"""
        self._binary_num = []
        if self._decimal_num == 0:
            self._binary_num = [0] * bits
            self._sign_bit = [0]
            return self._binary_num

        result = []
        n = self._decimal_num

        if self._decimal_num < 0:
            self._binary_num = [1]
            n *= -1
            self._sign_bit = [1]

        while n > 0:
            result.insert(0, n % 2)
            n //= 2
        self._binary_num = [0] * (bits - len(result)) + result

        return self._binary_num

    def bin_to_reverse_code(self) -> list[int]:
        """Перевод бинарного числа в обратный код"""
        self._reverse_code = []
        if self._sign_bit == [0]:
            self._reverse_code = self._binary_num
            return self._reverse_code
        
        for n in self._binary_num:
            if n == 0:
                self._reverse_code.append(1)
            else:
                self._reverse_code.append(0)

        return self._reverse_code  

    def rev_code_to_compl_code(self) -> list[int]:
        """Перевод обратного кода в дополнительный"""
        self._compl_code = []
        if self._sign_bit == [0]:
            self._compl_code = self._binary_num
            return self._compl_code
        
        overflow = 0
        one = [1] + [0] * 31
        rev_num = self._reverse_code[::-1]

        for buff in zip(one, rev_num):
            value = buff[0] + buff[1] + overflow
            overflow = value // 2
            self._compl_code.append(value % 2)
        
        self._compl_code = self._compl_code[::-1]

        return self._compl_code