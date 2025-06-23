def find_words_by_V(matrix, V_key, direction="top"):
    results = []
    for j in range(matrix.size):
        word = matrix.get_word(j)
        V = word[:len(V_key)]
        if V == V_key:
            results.append(j)
            if direction == "top":
                break
    if direction == "bottom" and results:
        results = [results[-1]]
    return results

def print_search_results(matrix, V_key):
    top = find_words_by_V(matrix, V_key, "top")
    bottom = find_words_by_V(matrix, V_key, "bottom")
    print(f"Найдено сверху: слово {top[0]}, V={int(''.join(map(str, V_key)), 2)} ({''.join(map(str, V_key))})" if top else "Не найдено")
    print(f"Найдено снизу: слово {bottom[0]}, V={int(''.join(map(str, V_key)), 2)} ({''.join(map(str, V_key))})" if bottom else "Не найдено")