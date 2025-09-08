from typing import List, Tuple, Dict, Set
from minimization.calculation import get_prime_implicants, find_minimal_cover, term_to_bin, bin_to_term, covers_minterm
from utils.table_printer import print_implicant_stages, print_coverage_table
from utils.common import term_to_string

def minimize_sknf_calc_table(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СКНФ расчётно-табличным методом."""
    maxterms = []
    for row in truth_table:
        if not row['result']:
            term = [(var, 1 if row[var] else 0) for var in variables]
            maxterms.append(term)
    
    if not maxterms:
        return "1"
    
    print("\nПоиск простых импликантов для СКНФ:")
    prime_implicants = get_prime_implicants(maxterms, variables, is_sknf=True)
    
    # Строим таблицу покрытия для вывода
    coverage = []
    for imp in prime_implicants:
        imp_coverage = []
        for mt in maxterms:
            covers = covers_minterm(imp, mt)
            imp_coverage.append(1 if covers else 0)
        coverage.append(imp_coverage)
    
    print("\nТаблица покрытия СКНФ:")
    print_coverage_table(prime_implicants, maxterms, coverage, is_sknf=True)
    
    # Находим минимальное покрытие
    minimal_cover = find_minimal_cover(prime_implicants, maxterms)
    
    result = [term_to_string(imp, is_sknf=True) for imp in minimal_cover]
    return " & ".join(f"({r})" for r in sorted(result)) if result else "1"

def minimize_sdnf_calc_table(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СДНФ расчётно-табличным методом."""
    minterms = []
    for row in truth_table:
        if row['result']:
            term = [(var, 1 if row[var] else 0) for var in variables]
            minterms.append(term)
    
    if not minterms:
        return "0"
    
    print("\nПоиск простых импликантов для СДНФ:")
    prime_implicants = get_prime_implicants(minterms, variables)
    
    # Строим таблицу покрытия для вывода
    coverage = []
    for imp in prime_implicants:
        imp_coverage = []
        for mt in minterms:
            covers = covers_minterm(imp, mt)
            imp_coverage.append(1 if covers else 0)
        coverage.append(imp_coverage)
    
    print("\nТаблица покрытия СДНФ:")
    print_coverage_table(prime_implicants, minterms, coverage)
    
    # Находим минимальное покрытие
    minimal_cover = find_minimal_cover(prime_implicants, minterms)
    
    result = [term_to_string(imp) for imp in minimal_cover]
    return " | ".join(f"({r})" for r in sorted(result)) if result else "0"

