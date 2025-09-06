from typing import List, Tuple, Dict
from utils.common import term_to_string

def print_truth_table(truth_table: List[Dict], variables: List[str]) -> None:
    """Выводит таблицу истинности."""
    header = variables + ["f"]
    print(" | ".join(header))
    print("-" * (len(variables) * 4 + 3))
    for row in truth_table:
        values = [str(int(row[var])) for var in variables] + [str(int(row['result']))]
        print(" | ".join(values))

def print_implicant_stages(stages: List[List[Tuple[str, int]]], is_sknf: bool = False) -> None:
    """Выводит стадии склеивания."""
    for i, stage in enumerate(stages):
        print(f"Стадия {i + 1}:")
        for term in stage:
            print(term_to_string(term, is_sknf))
        print()

def print_coverage_table(implicants: List[List[Tuple[str, int]]], minterms: List[List[Tuple[str, int]]], coverage: List[List[int]], is_sknf: bool = False) -> None:
    """Выводит таблицу покрытия."""
    header = ["Imp\\Min"] + [str(i) for i in range(len(minterms))]
    print(" | ".join(header))
    print("-" * (len(minterms) * 4 + 10))
    
    for i, imp in enumerate(implicants):
        row = [term_to_string(imp, is_sknf)] + [str(c) for c in coverage[i]]
        print(" | ".join(row))

def print_karnaugh_map(kmap: List[int], variables: List[str]) -> None:
    """Выводит карту Карно в виде таблицы."""
    n = len(variables)
    rows = 2**(n // 2)
    cols = 2**(n - n // 2)
    row_vars = variables[:n//2]
    col_vars = variables[n//2:]
    
    # Генерируем код Грея для строк и столбцов
    row_gray = generate_gray_code(len(row_vars)) if row_vars else [""]
    col_gray = generate_gray_code(len(col_vars)) if col_vars else [""]
    
    # Формируем заголовок
    header = [""] + [''.join(c) for c in col_gray]
    if col_vars:
        header[0] = ''.join(col_vars) + "\\" + ''.join(row_vars)
    print(" | ".join(header))
    print("-" * (len(header) * 4 + len(header) - 1))
    
    # Выводим таблицу
    for i, row_code in enumerate(row_gray):
        row = [row_code if row_vars else "0"]
        for j, col_code in enumerate(col_gray):
            idx = int(row_code + col_code, 2) if row_code or col_code else 0
            row.append(str(kmap[idx]))
        print(" | ".join(row))

def generate_gray_code(n: int) -> List[str]:
    """Генерирует код Грея для n бит."""
    if n == 0:
        return [""]
    first_half = generate_gray_code(n - 1)
    second_half = first_half[::-1]
    return ["0" + code for code in first_half] + ["1" + code for code in second_half]