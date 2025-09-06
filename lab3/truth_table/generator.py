from itertools import product

def generate_truth_table(root, variables):
    """
    Строит таблицу истинности по дереву выражения.
    """
    table = []
    for values in product([False, True], repeat=len(variables)):
        valuation = dict(zip(variables, values))
        result = root.evaluate(valuation)
        row = valuation.copy()
        row['result'] = result
        table.append(row)
    return table
