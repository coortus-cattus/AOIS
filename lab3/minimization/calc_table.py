from typing import List, Tuple, Dict
from minimization.calculation import term_to_bin, bin_to_term, covers_minterm
from utils.table_printer import print_implicant_stages, print_coverage_table
from utils.common import term_to_string

def minimize_sknf_calc_table(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СКНФ расчётно-табличным методом."""
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
    
    implicants = [bin_to_term(b, variables) for b in sorted(set(all_implicants_bin))]
    minterms = terms
    coverage = []
    for imp in implicants:
        imp_coverage = []
        for mt in minterms:
            covers = covers_minterm(imp, mt)
            imp_coverage.append(1 if covers else 0)
        coverage.append(imp_coverage)
    
    print("\nТаблица покрытия СКНФ:")
    print_coverage_table(implicants, minterms, coverage, is_sknf=True)
    
    selected = []
    covered = set()
    
    for j in range(len(minterms)):
        covering_imps = [(i, imp) for i, imp in enumerate(implicants) if coverage[i][j] == 1]
        if len(covering_imps) == 1:
            imp_idx, imp = covering_imps[0]
            if imp not in selected:
                selected.append(imp)
                covered.update(j for j in range(len(minterms)) if coverage[imp_idx][j] == 1)
    
    while len(covered) < len(minterms):
        best_imp = None
        best_count = -1
        best_covered = set()
        best_var_count = float('inf')
        for i, imp in enumerate(implicants):
            if imp in selected:
                continue
            new_covered = set(j for j in range(len(minterms)) if coverage[i][j] == 1 and j not in covered)
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
    
    result = [term_to_string(imp, is_sknf=True) for imp in selected]
    return " & ".join(f"({r})" for r in sorted(result)) if result else "1"

def minimize_sdnf_calc_table(truth_table: List[Dict], variables: List[str]) -> str:
    """Минимизация СДНФ расчётно-табличным методом."""
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
    coverage = []
    for imp in implicants:
        imp_coverage = []
        for mt in minterms:
            covers = covers_minterm(imp, mt)
            imp_coverage.append(1 if covers else 0)
        coverage.append(imp_coverage)
    
    print("\nТаблица покрытия СДНФ:")
    print_coverage_table(implicants, minterms, coverage)
    
    selected = []
    covered = set()
    
    for j in range(len(minterms)):
        covering_imps = [(i, imp) for i, imp in enumerate(implicants) if coverage[i][j] == 1]
        if len(covering_imps) == 1:
            imp_idx, imp = covering_imps[0]
            if imp not in selected:
                selected.append(imp)
                covered.update(j for j in range(len(minterms)) if coverage[imp_idx][j] == 1)
    
    while len(covered) < len(minterms):
        best_imp = None
        best_count = -1
        best_covered = set()
        best_var_count = float('inf')
        for i, imp in enumerate(implicants):
            if imp in selected:
                continue
            new_covered = set(j for j in range(len(minterms)) if coverage[i][j] == 1 and j not in covered)
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
    
    result = [term_to_string(imp) for imp in selected]
    return " | ".join(f"({r})" for r in sorted(result)) if result else "0"