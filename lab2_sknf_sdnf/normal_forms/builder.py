def build_sdnf(truth_table, variables):
    terms = []
    for row in truth_table:
        if row['result']:
            term_parts = []
            for var in variables:
                if row[var]:
                    term_parts.append(var)
                else:
                    term_parts.append(f"!{var}")
            terms.append("(" + " & ".join(term_parts) + ")")
    return " | ".join(terms) if terms else "0"


def build_sknf(truth_table, variables):
    clauses = []
    for row in truth_table:
        if not row['result']:
            clause_parts = []
            for var in variables:
                if row[var]:
                    clause_parts.append(f"!{var}")
                else:
                    clause_parts.append(var)
            clauses.append("(" + " | ".join(clause_parts) + ")")
    return " & ".join(clauses) if clauses else "1"
