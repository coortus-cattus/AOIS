from parser.logic_parser import parse_expression
from truth_table.generator import generate_truth_table
from normal_forms.builder import build_sdnf, build_sknf
from utils.expression_utils import get_numeric_form, get_index_form

def main():
    expr = None
    root = None
    variables = None
    truth_table = None

    while True:
        print("\n=== МЕНЮ ===")
        print("1. Ввести логическое выражение")
        print("2. Показать таблицу истинности")
        print("3. Построить СДНФ")
        print("4. Построить СКНФ")
        print("5. Числовая форма СДНФ")
        print("6. Числовая форма СКНФ")
        print("7. Индексная форма функции")
        print("8. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            expr = input("Введите логическое выражение: ")
            try:
                root, variables = parse_expression(expr)
                truth_table = generate_truth_table(root, variables)
                print("Выражение успешно разобрано!")
            except Exception as e:
                print(f"Ошибка при разборе выражения: {e}")
        elif choice == "2":
            if not truth_table:
                print("Сначала введите выражение.")
                continue
            print("\nТаблица истинности:")
            header = " | ".join(variables + ['result'])
            print(header)
            print("-" * len(header))
            for row in truth_table:
                print(" | ".join(['1' if row[v] else '0' for v in variables] + ['1' if row['result'] else '0']))
        elif choice == "3":
            if not truth_table:
                print("Сначала введите выражение.")
                continue
            sdnf = build_sdnf(truth_table, variables)
            print("СДНФ:", sdnf)
        elif choice == "4":
            if not truth_table:
                print("Сначала введите выражение.")
                continue
            sknf = build_sknf(truth_table, variables)
            print("СКНФ:", sknf)
        elif choice == '5':
            indices = get_numeric_form(root, variables, mode='sdnf')
            print(f"Числовая форма СДНФ: !({', '.join(map(str, indices))})")
        elif choice == '6':
            indices = get_numeric_form(root, variables, mode='sknf')
            print(f"Числовая форма СКНФ: &({', '.join(map(str, indices))})")
        elif choice == '7':
            binary = get_index_form(root, variables)
            print(f"Индексная форма: {binary}")
        elif choice == "8":
            print("Выход из программы.")
            break
        else:
            print("Неверный пункт меню")

if __name__ == "__main__":
    main()
