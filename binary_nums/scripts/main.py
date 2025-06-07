# main.py
from src.binary_codes import BinaryNumber
from src.ieee754 import IEEE754Float, add_ieee754
import src.utils as utils


def display_menu():
    print('-' * 58)
    print('Функции:')
    print('1. Перевести десятичное число в двоичный, обратный и дополнительный коды.')
    print('2. Сложить два числа в дополнительном коде.')
    print('3. Вычесть одно число из другого.')
    print('4. Умножить два числа в прямом коде.')
    print('5. Поделить одно число на другое.')
    print('6. Сложить два положительных числа с плавающей точкой (IEEE-754).')
    print('0. Выход.')
    print('-' * 58)


def input_integer(prompt: str) -> int:

    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Ошибка: Требуется целое число.')


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Ошибка: Требуется дробное число.')


def print_binary_number(num: BinaryNumber, label: str = 'Число'):
    print(f'{label}: {num.decimal_num}')
    utils.convert_all_tipes(num)
    print('Прямой код:        ', num.binary_num)
    print('Обратный код:      ', num.reverse_code)
    print('Дополнительный код:', num.compl_code)


def handle_binary_operation(choice: int, num1: BinaryNumber, num2: BinaryNumber):
    operations = {
        2: ('Сумма', utils.sum_in_compl_code, utils.twos_complement_to_decimal),
        3: ('Разность', utils.subtraction, utils.twos_complement_to_decimal),
        4: ('Произведение', utils.multiplication, utils.binary_to_decimal),
        5: ('Частное', utils.division, lambda x: x)  # Деление возвращает список
    }
    
    label, operation, converter = operations[choice]
    print_binary_number(num1, 'Число 1')
    print_binary_number(num2, 'Число 2')
    
    try:
        result = operation(num1, num2)
        if choice == 5:
            decimal_result = utils.binary_fraction_to_decimal(result)
            print(f'{label}: {decimal_result}')
            print('Прямой код:', result)
        else:
            result_num = BinaryNumber(converter(result))
            print_binary_number(result_num, label)
    except ValueError as e:
        print(f'Ошибка: {e}')


def main():
    while True:
        display_menu()
        try:
            choice = int(input('Введите 0-6 для выбора функции: '))
        except ValueError:
            print('Ошибка: Введите число от 0 до 6.')
            continue

        if choice == 0:
            print('Программа завершена.')
            return 0
        
        if choice == 1:
            n = input_integer('Введите целое число: ')
            num = BinaryNumber(n)
            print_binary_number(num)
        
        elif choice in (2, 3, 4, 5):
            n1 = input_integer('Введите первое целое число: ')
            num1 = BinaryNumber(n1)
            n2 = input_integer('Введите второе целое число: ')
            num2 = BinaryNumber(n2)
            handle_binary_operation(choice, num1, num2)
        
        elif choice == 6:
            n1 = input_float('Введите первое дробное число: ')
            try:
                num1 = IEEE754Float.from_decimal(n1)
            except ValueError as e:
                print(f'Ошибка: {e}')
                continue
                
            n2 = input_float('Введите второе дробное число: ')
            try:
                num2 = IEEE754Float.from_decimal(n2)
            except ValueError as e:
                print(f'Ошибка: {e}')
                continue
            
            try:
                result = add_ieee754(num1, num2)
                decimal_result = result.to_decimal()
                print(f'Число 1: {num1.to_decimal()} ({num1.to_bits()})')
                print(f'Число 2: {num2.to_decimal()} ({num2.to_bits()})')
                print(f'Сумма: {decimal_result} ({result.to_bits()})')
            except ValueError as e:
                print(f'Ошибка: {e}')


if __name__ == '__main__':
    main()