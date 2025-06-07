from itertools import product

def get_index_form(root, variables, full_output=False):
    results = []
    for values in product([False, True], repeat=len(variables)):
        context = dict(zip(variables, values))
        result = root.evaluate(context)
        bin_str = ''.join(['1' if v else '0' for v in values])
        if full_output:
            results.append((bin_str, int(result)))
        else:
            results.append(str(int(result)))
    if full_output:
        return results
    return ''.join(results)

def get_numeric_form(root, variables, mode='sdnf'):
    indices = []
    for idx, values in enumerate(product([False, True], repeat=len(variables))):
        context = dict(zip(variables, values))
        result = root.evaluate(context)
        if mode == 'sdnf' and result:
            indices.append(idx)
        elif mode == 'sknf' and not result:
            indices.append(idx)
    return indices


