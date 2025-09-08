from typing import List, Dict, Tuple, Set
from utils.table_printer import print_karnaugh_map
from utils.common import term_to_string

def generate_gray_code(n: int) -> List[str]:
    """Генерирует код Грея для n бит."""
    if n == 0:
        return [""]
    first_half = generate_gray_code(n - 1)
    second_half = first_half[::-1]
    return ["0" + code for code in first_half] + ["1" + code for code in second_half]

def build_karnaugh_map(truth_table: List[Dict], variables: List[str], is_sknf: bool = False) -> tuple:
    """Строит карту Карно для 2-5 переменных."""
    n = len(variables)
    if n > 5:
        print("Карта Карно поддерживает до 5 переменных")
        return None, None, 0, 0, [], [], [], []
    
    # Определяем размеры карты для 2-5 переменных
    if n == 1:
        rows, cols = 1, 2
        row_vars, col_vars = [], variables
    elif n == 2:
        rows, cols = 2, 2
        row_vars, col_vars = [variables[0]], [variables[1]]
    elif n == 3:
        rows, cols = 2, 4
        row_vars, col_vars = [variables[0]], variables[1:]
    elif n == 4:
        rows, cols = 4, 4
        row_vars, col_vars = variables[:2], variables[2:]
    else:  # n == 5
        rows, cols = 4, 8
        row_vars, col_vars = variables[:2], variables[2:]
    
    # Генерируем коды Грея
    gray_rows = generate_gray_code(len(row_vars))
    gray_cols = generate_gray_code(len(col_vars))
    
    kmap_2d = [[0 for _ in range(cols)] for _ in range(rows)]
    kmap_flat = [0 for _ in range(rows * cols)]
    
    # Заполняем карту
    for row_idx in range(rows):
        for col_idx in range(cols):
            # Получаем значения переменных из позиции в карте
            row_code = gray_rows[row_idx] if row_vars else ""
            col_code = gray_cols[col_idx] if col_vars else ""
            
            # Создаем valuation для этой ячейки
            valuation = {}
            for i, var in enumerate(variables):
                if i < len(row_code):
                    valuation[var] = bool(int(row_code[i]))
                elif i - len(row_code) < len(col_code):
                    valuation[var] = bool(int(col_code[i - len(row_code)]))
            
            # Находим соответствующий результат в таблице истинности
            for table_row in truth_table:
                match = True
                for var in variables:
                    if table_row[var] != valuation.get(var, False):
                        match = False
                        break
                if match:
                    value = table_row['result']
                    # Правильное заполнение карты
                    if is_sknf:
                        kmap_2d[row_idx][col_idx] = 0 if not value else 1
                    else:
                        kmap_2d[row_idx][col_idx] = 1 if value else 0
                    kmap_flat[row_idx * cols + col_idx] = kmap_2d[row_idx][col_idx]
                    break
    
    return kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols

def find_maximal_rectangles(kmap_2d: List[List[int]], target: int = 1) -> List[Set[Tuple[int, int]]]:
    """Находит максимальные прямоугольники целевых значений."""
    rows, cols = len(kmap_2d), len(kmap_2d[0])
    groups = []
    visited = set()
    
    def is_valid_rectangle(start_r, start_c, height, width):
        """Проверяет, является ли прямоугольник valid."""
        for dr in range(height):
            for dc in range(width):
                r = (start_r + dr) % rows
                c = (start_c + dc) % cols
                if kmap_2d[r][c] != target:
                    return False
        return True
    
    def expand_rectangle(start_r, start_c):
        """Расширяет прямоугольник максимально возможного размера."""
        max_height, max_width = 1, 1
        
        # Расширяем по высоте
        for height in range(1, rows + 1):
            if not is_valid_rectangle(start_r, start_c, height, 1):
                break
            max_height = height
        
        # Расширяем по ширине для каждой возможной высоты
        best_area = 0
        best_rect = None
        
        for h in range(1, max_height + 1):
            for w in range(1, cols + 1):
                if is_valid_rectangle(start_r, start_c, h, w):
                    area = h * w
                    if area > best_area:
                        best_area = area
                        best_rect = (h, w)
        
        if best_rect:
            h, w = best_rect
            cells = set()
            for dr in range(h):
                for dc in range(w):
                    r = (start_r + dr) % rows
                    c = (start_c + dc) % cols
                    cells.add((r, c))
            return cells
        return None
    
    # Ищем максимальные прямоугольники для каждой ячейки
    for r in range(rows):
        for c in range(cols):
            if kmap_2d[r][c] == target and (r, c) not in visited:
                rect = expand_rectangle(r, c)
                if rect:
                    # Проверяем, не является ли этот прямоугольник подмножеством уже найденного
                    is_subset = False
                    for existing in groups:
                        if rect.issubset(existing):
                            is_subset = True
                            break
                    
                    if not is_subset:
                        # Удаляем все подмножества нового прямоугольника
                        groups = [g for g in groups if not g.issubset(rect)]
                        groups.append(rect)
                        visited.update(rect)
    
    return groups

def find_essential_groups(kmap_2d: List[List[int]], target: int = 1) -> List[Set[Tuple[int, int]]]:
    """Находит минимальное покрытие."""
    rows, cols = len(kmap_2d), len(kmap_2d[0])
    
    # Находим все ячейки с target
    target_cells = set()
    for r in range(rows):
        for c in range(cols):
            if kmap_2d[r][c] == target:
                target_cells.add((r, c))
    
    if not target_cells:
        return []
    
    # Находим все максимальные группы
    all_groups = find_maximal_rectangles(kmap_2d, target)
    
    # Жадный алгоритм покрытия
    covered = set()
    selected_groups = []
    
    while covered != target_cells:
        best_group = None
        best_coverage = 0
        
        for group in all_groups:
            if group in selected_groups:
                continue
            new_coverage = len(group - covered)
            if new_coverage > best_coverage:
                best_coverage = new_coverage
                best_group = group
        
        if best_group is None:
            break
            
        selected_groups.append(best_group)
        covered |= best_group
    
    return selected_groups

def group_to_term(group: Set[Tuple[int, int]], row_vars: List[str], col_vars: List[str], 
                 gray_rows: List[str], gray_cols: List[str], is_sknf: bool = False) -> List[Tuple[str, int]]:
    """Преобразует группу ячеек в логический терм."""
    if not group:
        return []
    
    constant_vars = {}
    
    # Анализируем строки
    if row_vars:
        rows_covered = set(r for r, c in group)
        for i, var in enumerate(row_vars):
            values = set()
            for row in rows_covered:
                if row < len(gray_rows) and i < len(gray_rows[row]):
                    values.add(int(gray_rows[row][i]))
            
            if len(values) == 1:
                value = values.pop()
                if is_sknf:
                    constant_vars[var] = 0 if value == 0 else 1
                else:
                    constant_vars[var] = 1 if value == 1 else 0
    
    # Анализируем столбцы
    if col_vars:
        cols_covered = set(c for r, c in group)
        for i, var in enumerate(col_vars):
            values = set()
            for col in cols_covered:
                if col < len(gray_cols) and i < len(gray_cols[col]):
                    values.add(int(gray_cols[col][i]))
            
            if len(values) == 1:
                value = values.pop()
                if is_sknf:
                    constant_vars[var] = 0 if value == 0 else 1
                else:
                    constant_vars[var] = 1 if value == 1 else 0
    
    return [(var, val) for var, val in constant_vars.items()]

def minimize_sknf_karnaugh(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СКНФ с помощью карты Карно."""
    result = build_karnaugh_map(truth_table, variables, is_sknf=True)
    if result[0] is None:
        return "1"
    
    kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols = result
    
    print("\nКарта Карно для СКНФ:")
    print_karnaugh_map(kmap_flat, row_vars + col_vars)
    
    # Для СКНФ ищем группы НУЛЕЙ
    groups = find_essential_groups(kmap_2d, target=0)
    
    # Преобразуем группы в термы
    terms = []
    for group in groups:
        term = group_to_term(group, row_vars, col_vars, gray_rows, gray_cols, is_sknf=True)
        if term:
            terms.append(term)
    
    result_terms = [term_to_string(term, is_sknf=True) for term in terms]
    return " & ".join(f"({r})" for r in sorted(result_terms)) if result_terms else "1"

def minimize_sdnf_karnaugh(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СДНФ с помощью карты Карно."""
    result = build_karnaugh_map(truth_table, variables, is_sknf=False)
    if result[0] is None:
        return "0"
    
    kmap_2d, kmap_flat, rows, cols, row_vars, col_vars, gray_rows, gray_cols = result
    
    print("\nКарта Карно для СДНФ:")
    print_karnaugh_map(kmap_flat, row_vars + col_vars)
    
    # Для СДНФ ищем группы ЕДИНИЦ
    groups = find_essential_groups(kmap_2d, target=1)
    
    # Преобразуем группы в термы
    terms = []
    for group in groups:
        term = group_to_term(group, row_vars, col_vars, gray_rows, gray_cols, is_sknf=False)
        if term:
            terms.append(term)
    
    result_terms = [term_to_string(term) for term in terms]
    return " | ".join(f"({r})" for r in sorted(result_terms)) if result_terms else "0"