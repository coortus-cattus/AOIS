from typing import List, Tuple, Dict, Set
from itertools import product, combinations
from utils.table_printer import print_implicant_stages
from utils.common import term_to_string

def term_to_bin(term: List[Tuple[str, int]], variables: List[str]) -> str:
    """Преобразует терм в бинарную строку ('0', '1', '_')."""
    bin_str = ''
    for var in variables:
        found = False
        for v, val in term:
            if v == var:
                bin_str += '_' if val is None else str(val)
                found = True
                break
        if not found:
            bin_str += '_'
    return bin_str

def bin_to_term(bin_str: str, variables: List[str]) -> List[Tuple[str, int]]:
    """Преобразует бинарную строку в терм."""
    term = []
    for i, char in enumerate(bin_str):
        if char != '_':
            term.append((variables[i], int(char)))
    return term

def covers_minterm(implicant: List[Tuple[str, int]], minterm: List[Tuple[str, int]]) -> bool:
    """Проверяет, покрывает ли импликант минтерм."""
    imp_dict = {var: val for var, val in implicant if val is not None}
    for var, val in minterm:
        if var in imp_dict and imp_dict[var] != val:
            return False
    return True

def get_prime_implicants(terms: List[List[Tuple[str, int]]], variables: List[str], is_sknf: bool = False) -> List[List[Tuple[str, int]]]:
    """Находит все простые импликанты используя метод Квайна-Мак-Класки."""
    if not terms:
        return []
    
    # Преобразуем термы в бинарный формат
    bin_terms = [term_to_bin(term, variables) for term in terms]
    current_stage = bin_terms
    prime_implicants_bin = set()
    stages_bin = [current_stage]
    
    while current_stage:
        used_indices = set()
        next_stage = []
        
        # Пытаемся склеить все возможные пары термов
        for i in range(len(current_stage)):
            for j in range(i + 1, len(current_stage)):
                term1 = current_stage[i]
                term2 = current_stage[j]
                
                # Проверяем, можно ли склеить термы
                diff_count = 0
                diff_pos = -1
                
                for k in range(len(term1)):
                    if term1[k] != term2[k]:
                        if term1[k] != '_' and term2[k] != '_':
                            diff_count += 1
                            diff_pos = k
                        else:
                            # Если один из термов уже имеет '_' в этой позиции, а другой - нет
                            diff_count = 2  # Нельзя склеить
                            break
                
                if diff_count == 1:
                    used_indices.add(i)
                    used_indices.add(j)
                    new_term = list(term1)
                    new_term[diff_pos] = '_'
                    new_term_str = ''.join(new_term)
                    if new_term_str not in next_stage:
                        next_stage.append(new_term_str)
        
        # Добавляем неиспользованные термы в простые импликанты
        for idx in range(len(current_stage)):
            if idx not in used_indices:
                prime_implicants_bin.add(current_stage[idx])
        
        if not next_stage:
            break
            
        # Переходим к следующей стадии
        current_stage = next_stage
        stages_bin.append(current_stage)
    
    # Преобразуем обратно в термы
    prime_implicants = [bin_to_term(bin_str, variables) for bin_str in prime_implicants_bin]
    
    # Выводим стадии склеивания для отладки
    stages_terms = [[bin_to_term(b, variables) for b in stage] for stage in stages_bin]
    if is_sknf:
        print_implicant_stages(stages_terms, is_sknf=True)
    else:
        print_implicant_stages(stages_terms)
    
    return prime_implicants

def find_minimal_cover(prime_implicants: List[List[Tuple[str, int]]], 
                      minterms: List[List[Tuple[str, int]]]) -> List[List[Tuple[str, int]]]:
    """Находит минимальное покрытие используя алгоритм Петрика."""
    if not minterms:
        return []
    
    # Строим таблицу покрытия
    coverage_table = []
    for imp in prime_implicants:
        row = []
        for minterm in minterms:
            row.append(1 if covers_minterm(imp, minterm) else 0)
        coverage_table.append(row)
    
    # Находим существенные импликанты
    essential_implicants = []
    covered_minterms = set()
    
    for j in range(len(minterms)):
        covering_imps = []
        for i in range(len(prime_implicants)):
            if coverage_table[i][j] == 1:
                covering_imps.append(i)
        
        if len(covering_imps) == 1:
            imp_idx = covering_imps[0]
            if prime_implicants[imp_idx] not in essential_implicants:
                essential_implicants.append(prime_implicants[imp_idx])
                # Отмечаем покрытые минтермы
                for k in range(len(minterms)):
                    if coverage_table[imp_idx][k] == 1:
                        covered_minterms.add(k)
    
    # Если все минтермы покрыты существенными импликантами
    if len(covered_minterms) == len(minterms):
        return essential_implicants
    
    # Удаляем уже покрытые минтермы и существенные импликанты
    remaining_minterms = [minterms[i] for i in range(len(minterms)) if i not in covered_minterms]
    remaining_imps = []
    remaining_coverage = []
    
    for i, imp in enumerate(prime_implicants):
        if imp not in essential_implicants:
            remaining_imps.append(imp)
            row = []
            for j in range(len(minterms)):
                if j not in covered_minterms and coverage_table[i][j] == 1:
                    row.append(1)
                else:
                    row.append(0)
            remaining_coverage.append(row)
    
    if not remaining_minterms:
        return essential_implicants
    
    # Используем алгоритм Петрика для оставшихся минтермов
    # Формируем продукт сумм для алгоритма Петрика
    petrick_products = []
    for j in range(len(remaining_minterms)):
        product_terms = []
        for i in range(len(remaining_imps)):
            if remaining_coverage[i][j] == 1:
                product_terms.append({i})
        petrick_products.append(product_terms)
    
    # Комбинируем продукты
    if petrick_products:
        result_products = petrick_products[0]
        for i in range(1, len(petrick_products)):
            new_products = []
            for prod1 in result_products:
                for prod2 in petrick_products[i]:
                    new_products.append(prod1 | prod2)
            # Удаляем дубликаты и доминируемые множества
            result_products = []
            for prod in new_products:
                if prod not in result_products:
                    # Проверяем, не доминируется ли это множество
                    to_add = True
                    for existing in result_products[:]:
                        if existing.issubset(prod):
                            result_products.remove(existing)
                        elif prod.issubset(existing):
                            to_add = False
                            break
                    if to_add:
                        result_products.append(prod)
    
    # Выбираем множество с наименьшим количеством импликантов
    if petrick_products and result_products:
        best_set = min(result_products, key=len)
        selected_remaining = [remaining_imps[i] for i in best_set]
    else:
        selected_remaining = []
    
    return essential_implicants + selected_remaining

def minimize_sdnf_calculation(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СДНФ расчётным методом."""
    # Получаем минтермы из таблицы истинности
    minterms = []
    for row in truth_table:
        if row['result']:
            term = [(var, 1 if row[var] else 0) for var in variables]
            minterms.append(term)
    
    if not minterms:
        return "0"
    
    print("\nПоиск простых импликантов для СДНФ:")
    # Находим все простые импликанты
    prime_implicants = get_prime_implicants(minterms, variables)
    
    # Находим минимальное покрытие
    minimal_cover = find_minimal_cover(prime_implicants, minterms)
    
    # Формируем результат
    result_terms = [term_to_string(term) for term in minimal_cover]
    return " | ".join(f"({r})" for r in sorted(result_terms)) if result_terms else "0"

def minimize_sknf_calculation(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СКНФ расчётным методом."""
    # Получаем макстермы из таблицы истинности
    maxterms = []
    for row in truth_table:
        if not row['result']:
            term = [(var, 1 if row[var] else 0) for var in variables]
            maxterms.append(term)
    
    if not maxterms:
        return "1"
    
    print("\nПоиск простых импликантов для СКНФ:")
    # Находим все простые импликанты (для СКНФ алгоритм аналогичен)
    prime_implicants = get_prime_implicants(maxterms, variables, is_sknf=True)
    
    # Находим минимальное покрытие
    minimal_cover = find_minimal_cover(prime_implicants, maxterms)
    
    # Формируем результат
    result_terms = [term_to_string(term, is_sknf=True) for term in minimal_cover]
    return " & ".join(f"({r})" for r in sorted(result_terms)) if result_terms else "1"


