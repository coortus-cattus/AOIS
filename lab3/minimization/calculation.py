from typing import List, Tuple, Dict
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

def minimize_sknf_calculation(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СКНФ расчётным методом."""
    terms = []
    for row in truth_table:
        if not row['result']:
            term = [(var, 1 if row[var] else 0) for var in variables]
            terms.append(term)
    
    if not terms:
        return "1"
    
    print("\nСтадии склеивания СКНФ:")
    bin_terms = [term_to_bin(term, variables) for term in terms]
    stages_bin = [bin_terms]
    all_implicants_bin = bin_terms.copy()
    
    while True:
        new_terms = []
        used_in_stage = set()
        for i, term1 in enumerate(stages_bin[-1]):
            for j, term2 in enumerate(stages_bin[-1][i+1:], i+1):
                diff = 0
                diff_pos = -1
                for k in range(len(term1)):
                    if term1[k] != term2[k] and term1[k] != '_' and term2[k] != '_':
                        diff += 1
                        diff_pos = k
                if diff == 1:
                    used_in_stage.add(i)
                    used_in_stage.add(j)
                    new_term = list(term1)
                    new_term[diff_pos] = '_'
                    new_terms.append(''.join(new_term))
        
        for i, term in enumerate(stages_bin[-1]):
            if i not in used_in_stage:
                new_terms.append(term)
        
        new_terms = sorted(list(set(new_terms)))
        all_implicants_bin.extend(new_terms)
        
        if len(new_terms) == len(stages_bin[-1]) or not new_terms:
            break
        
        stages_bin.append(new_terms)
    
    stages = [[bin_to_term(b, variables) for b in stage] for stage in stages_bin]
    print_implicant_stages(stages, is_sknf=True)
    
    result = []
    for term in stages[-1]:
        result.append(term_to_string(term, is_sknf=True))
    return " & ".join(f"({r})" for r in sorted(result)) if result else "1"

def minimize_sdnf_calculation(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СДНФ расчётным методом."""
    terms = []
    for row in truth_table:
        if row['result']:
            term = [(var, 1 if row[var] else 0) for var in variables]
            terms.append(term)
    
    if not terms:
        return "0"
    
    print("\nСтадии склеивания СДНФ:")
    bin_terms = [term_to_bin(term, variables) for term in terms]
    stages_bin = [bin_terms]
    all_implicants_bin = bin_terms.copy()
    
    while True:
        new_terms = []
        used_in_stage = set()
        for i, term1 in enumerate(stages_bin[-1]):
            for j, term2 in enumerate(stages_bin[-1][i+1:], i+1):
                diff = 0
                diff_pos = -1
                for k in range(len(term1)):
                    if term1[k] != term2[k] and term1[k] != '_' and term2[k] != '_':
                        diff += 1
                        diff_pos = k
                if diff == 1:
                    used_in_stage.add(i)
                    used_in_stage.add(j)
                    new_term = list(term1)
                    new_term[diff_pos] = '_'
                    new_terms.append(''.join(new_term))
        
        for i, term in enumerate(stages_bin[-1]):
            if i not in used_in_stage:
                new_terms.append(term)
        
        new_terms = sorted(list(set(new_terms)))
        all_implicants_bin.extend(new_terms)
        
        if len(new_terms) == len(stages_bin[-1]) or not new_terms:
            break
        
        stages_bin.append(new_terms)
    
    stages = [[bin_to_term(b, variables) for b in stage] for stage in stages_bin]
    print_implicant_stages(stages)
    
    implicants = [bin_to_term(b, variables) for b in sorted(set(all_implicants_bin))]
    minterms = terms
    selected = []
    covered = set()
    
    # Выбираем существенные импликанты
    for j in range(len(minterms)):
        covering_imps = [(i, imp) for i, imp in enumerate(implicants) if covers_minterm(imp, minterms[j])]
        if len(covering_imps) == 1:
            imp_idx, imp = covering_imps[0]
            if imp not in selected:
                selected.append(imp)
                covered.update(j for j in range(len(minterms)) if covers_minterm(imp, minterms[j]))
    
    # Покрываем оставшиеся минтермы, отдавая приоритет импликантам с меньшим числом переменных
    while len(covered) < len(minterms):
        best_imp = None
        best_count = -1
        best_covered = set()
        best_var_count = float('inf')
        for i, imp in enumerate(implicants):
            if imp in selected:
                continue
            new_covered = set(j for j in range(len(minterms)) if covers_minterm(imp, minterms[j]) and j not in covered)
            count = len(new_covered)
            var_count = len([v for v, _ in imp])
            if count > 0 and (count > best_count or (count == best_count and var_count < best_var_count)):
                best_count = count
                best_imp = imp
                best_covered = new_covered
                best_var_count = var_count
        if best_imp is None:
            break
        selected.append(best_imp)
        covered.update(best_covered)
    
    result = [term_to_string(term) for term in selected]
    return " | ".join(f"({r})" for r in sorted(result)) if result else "0"