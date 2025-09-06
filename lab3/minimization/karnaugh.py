from typing import List, Dict, Tuple
from utils.table_printer import print_karnaugh_map
from utils.common import term_to_string

def generate_gray_code(n: int) -> List[str]:
    """Генерирует код Грея для n бит."""
    if n == 0:
        return [""]
    first_half = generate_gray_code(n - 1)
    second_half = first_half[::-1]
    return ["0" + code for code in first_half] + ["1" + code for code in second_half]

def build_karnaugh_map(truth_table: List[Dict], variables: List[str], is_sknf: bool = False) -> tuple[List[List[int]], List[int], int, int, List[str], List[str], List[str], List[str]]:
    """Строит карту Карно: двумерный для групп, плоский для печати."""
    n = len(variables)
    if n > 5:
        print("Карта Карно поддерживает только 2-5 переменных")
        return None, None, 0, 0, [], [], [], []
    
    if n == 2:
        rows, cols = 2, 2
        row_vars = [variables[0]]
        col_vars = [variables[1]]
    elif n == 3:
        rows, cols = 2, 4
        row_vars = [variables[0]]
        col_vars = [variables[1], variables[2]]
    elif n == 4:
        rows, cols = 4, 4
        row_vars = [variables[0], variables[1]]
        col_vars = [variables[2], variables[3]]
    else:
        rows, cols = 4, 8
        row_vars = [variables[0], variables[1]]
        col_vars = [variables[2], variables[3], variables[4]]
    
    kmap_2d = [[0 for _ in range(cols)] for _ in range(rows)]
    kmap_flat = [0 for _ in range(rows * cols)]
    gray_rows = ["0", "1"] if rows == 2 else ["00", "01", "11", "10"]
    gray_cols = (
        ["0", "1"] if cols == 2 else
        ["00", "01", "11", "10"] if cols == 4 else
        ["000", "001", "011", "010", "110", "111", "101", "100"]
    )
    
    for row in truth_table:
        values = {var: 1 if row[var] else 0 for var in variables}
        if n == 2:
            r, c = values[variables[0]], values[variables[1]]
        elif n == 3:
            r = values[variables[0]]
            col_bin = f"{values[variables[1]]}{values[variables[2]]}"
            c = {"00": 0, "01": 1, "11": 3, "10": 2}[col_bin]  # Исправлен порядок для кода Грея
        elif n == 4:
            row_bin = f"{values[variables[0]]}{values[variables[1]]}"
            col_bin = f"{values[variables[2]]}{values[variables[3]]}"
            r = {"00": 0, "01": 1, "11": 2, "10": 3}[row_bin]
            c = {"00": 0, "01": 1, "11": 2, "10": 3}[col_bin]
        else:
            row_bin = f"{values[variables[0]]}{values[variables[1]]}"
            col_bin = f"{values[variables[2]]}{values[variables[3]]}{values[variables[4]]}"
            r = {"00": 0, "01": 1, "11": 2, "10": 3}[row_bin]
            c = {
                "000": 0, "001": 1, "011": 2, "010": 3,
                "110": 4, "111": 5, "101": 6, "100": 7
            }[col_bin]
        kmap_2d[r][c] = 1 if is_sknf and not row['result'] else 0 if is_sknf else 1 if row['result'] else 0
        kmap_flat[r * cols + c] = kmap_2d[r][c]
    
    return kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols

def find_groups(kmap_2d: List[List[int]], n_vars: int, variables: List[str], rows: int, cols: int, gray_rows: List[str], gray_cols: List[str], is_sknf: bool = False) -> List[List[Tuple[str, int]]]:
    """Находит группы в карте Карно."""
    target = 1
    groups = []
    possible_sizes = [8, 4, 2, 1] if n_vars > 2 else [4, 2, 1]
    minterms = [(r, c) for r in range(rows) for c in range(cols) if kmap_2d[r][c] == target]
    
    # Генерируем все возможные группы
    for size in possible_sizes:
        if size > rows * cols:
            continue
        for h in [1, 2, 4] if size > 1 else [1]:
            for w in [size // h] if h * (size // h) == size else []:
                for r in range(rows):
                    for c in range(cols):
                        cells = set()
                        valid = True
                        for i in range(h):
                            for j in range(w):
                                i_mod = (r + i) % rows
                                j_mod = (c + j) % cols
                                if kmap_2d[i_mod][j_mod] != target:
                                    valid = False
                                    break
                                cells.add((i_mod, j_mod))
                            if not valid:
                                break
                        if valid and cells and len(cells) == size:
                            # Проверяем, что группа покрывает только минтермы
                            if all(cell in minterms for cell in cells):
                                # Вычисляем терм для группы
                                term = []
                                for var_idx, var in enumerate(variables):
                                    values = set()
                                    for gr, gc in cells:
                                        if n_vars == 3:
                                            bin_str = f"{gr}{gray_cols[gc]}"
                                        else:
                                            bin_str = f"{gray_rows[gr]}{gray_cols[gc]}"
                                        values.add(int(bin_str[var_idx]))
                                    if len(values) == 1:
                                        val = values.pop()
                                        term_val = 0 if is_sknf else 1
                                        if (is_sknf and val == 1) or (not is_sknf and val == 0):
                                            term_val = 1 - term_val
                                        term.append((var, term_val))
                                var_count = len(term)
                                # Для СДНФ исключаем группы с var_count=1, если есть альтернативы
                                if not is_sknf and var_count == 1 and any(len(g[3]) >= 2 for g in groups):
                                    continue
                                groups.append((cells, size, var_count, term))
    
    essential_groups = []
    covered_minterms = set()
    
    # Выбираем существенные импликанты
    for mt in minterms:
        covering_groups = [(g, s, v, t) for g, s, v, t in groups if mt in g]
        if len(covering_groups) == 1:
            group, size, var_count, term = covering_groups[0]
            if group not in [g for g, _, _, _ in essential_groups]:
                essential_groups.append((group, size, var_count, term))
                covered_minterms.update(group)
    
    # Покрываем оставшиеся минтермы
    while len(covered_minterms) < len(minterms):
        best_group = None
        best_count = -1
        best_covered = set()
        best_var_count = float('inf')
        for group, size, var_count, term in groups:
            if group in [g for g, _, _, _ in essential_groups]:
                continue
            new_covered = group - covered_minterms
            count = len(new_covered)
            # Предпочитаем группы с меньшим числом переменных, но для СДНФ var_count >= 2
            if count > 0 and (var_count < best_var_count or (var_count == best_var_count and count > best_count)) and (is_sknf or var_count >= 2):
                best_count = count
                best_group = group
                best_covered = new_covered
                best_var_count = var_count
                best_term = term
        if best_group is None:
            break
        essential_groups.append((best_group, size, best_var_count, best_term))
        covered_minterms.update(best_covered)
    
    result = [term for _, _, _, term in essential_groups if term]
    
    return sorted(result, key=lambda x: term_to_string(x, is_sknf))

def minimize_sknf_karnaugh(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СКНФ с помощью карты Карно."""
    kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols = build_karnaugh_map(truth_table, variables, is_sknf=True)
    if kmap_2d is None:
        return "1"
    
    print("\nКарта Карно для СКНФ:")
    print_karnaugh_map(kmap_flat, row_vars + col_vars)
    
    groups = find_groups(kmap_2d, len(variables), variables, rows, cols, gray_rows, gray_cols, is_sknf=True)
    
    result = [term_to_string(group, is_sknf=True) for group in groups]
    return " & ".join(f"({r})" for r in sorted(result)) if result else "1"

def minimize_sdnf_karnaugh(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СДНФ с помощью карты Карно."""
    kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols = build_karnaugh_map(truth_table, variables)
    if kmap_2d is None:
        return "0"
    
    print("\nКарта Карно для СДНФ:")
    print_karnaugh_map(kmap_flat, row_vars + col_vars)
    
    groups = find_groups(kmap_2d, len(variables), variables, rows, cols, gray_rows, gray_cols)
    
    result = [term_to_string(group) for group in groups]
    return " | ".join(f"({r})" for r in sorted(result)) if result else "0"