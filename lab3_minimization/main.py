from parser import parse_expression
from dnf_cnf_builder import generate_truth_table, build_sdnf
from utils import convert_to_implicants
from minimization import minimize_dnf_calc

def main():
    expression = input("Введите логическое выражение (например, !(!a->!b)|c): ")
    try:
        root, variables = parse_expression(expression)
        truth_table = generate_truth_table(root, variables)
        
        # Получаем СДНФ и преобразуем в импликанты
        sdnf = build_sdnf(truth_table, variables)
        sdnf_implicants = convert_to_implicants(sdnf, is_dnf=True)
        print("СДНФ:", sdnf)
        print("Импликанты СДНФ:", sdnf_implicants)
        
        # Минимизация с удалением лишних импликант
        minimized_dnf = minimize_dnf_calc(sdnf_implicants, variables)
        print("Минимизированная СДНФ:", minimized_dnf)
        
    except SyntaxError as e:
        print(f"Ошибка синтаксиса: {e}")

if __name__ == "__main__":
    main()