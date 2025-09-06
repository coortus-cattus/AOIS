from parser.logic_parser import parse_expression
from truth_table.generator import generate_truth_table
from normal_forms.builder import build_sknf, build_sdnf
from minimization.calculation import minimize_sknf_calculation, minimize_sdnf_calculation
from minimization.calc_table import minimize_sknf_calc_table, minimize_sdnf_calc_table
from minimization.karnaugh import minimize_sknf_karnaugh, minimize_sdnf_karnaugh
from utils.table_printer import print_truth_table

def main():
    # Ввод выражения
    expression = input("Введите логическое выражение (например, !(!a→!b)∨c): ")
    
    # Парсинг выражения
    root, variables = parse_expression(expression)
    
    # Построение таблицы истинности
    truth_table = generate_truth_table(root, variables)
    print("\nТаблица истинности:")
    print_truth_table(truth_table, variables)
    
    # Построение СКНФ и СДНФ
    sknf = build_sknf(truth_table, variables)
    sdnf = build_sdnf(truth_table, variables)
    print("\nСКНФ:", sknf)
    print("СДНФ:", sdnf)
    
    # Минимизация СКНФ
    print("\n=== Минимизация СКНФ ===")
    print("\nРасчётный метод:")
    min_sknf_calc = minimize_sknf_calculation(truth_table, variables)
    print("Результат:", min_sknf_calc)
    
    print("\nРасчётно-табличный метод:")
    min_sknf_calc_table = minimize_sknf_calc_table(truth_table, variables)
    print("Результат:", min_sknf_calc_table)
    
    print("\nТабличный метод (карта Карно):")
    min_sknf_karnaugh = minimize_sknf_karnaugh(truth_table, variables)
    print("Результат:", min_sknf_karnaugh)
    
    # Минимизация СДНФ
    print("\n=== Минимизация СДНФ ===")
    print("\nРасчётный метод:")
    min_sdnf_calc = minimize_sdnf_calculation(truth_table, variables)
    print("Результат:", min_sdnf_calc)
    
    print("\nРасчётно-табличный метод:")
    min_sdnf_calc_table = minimize_sdnf_calc_table(truth_table, variables)
    print("Результат:", min_sdnf_calc_table)
    
    print("\nТабличный метод (карта Карно):")
    min_sdnf_karnaugh = minimize_sdnf_karnaugh(truth_table, variables)
    print("Результат:", min_sdnf_karnaugh)

if __name__ == "__main__":
    main()