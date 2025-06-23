def extract_fields(word, v_bits=3, a_bits=4, b_bits=4):
    """Извлекает поля V, A, B из слова"""
    V = word[:v_bits]
    A = word[v_bits:v_bits+a_bits]
    B = word[v_bits+a_bits:v_bits+a_bits+b_bits]
    return V, A, B

def add_fields(A, B):
    """Складывает два бинарных поля и возвращает десятичную сумму"""
    a_int = int(''.join(map(str, A)), 2)
    b_int = int(''.join(map(str, B)), 2)
    return a_int + b_int

def print_words_info(matrix):
    """Выводит информацию о всех словах матрицы"""
    print("Слова (V, A, B):")
    for j in range(matrix.size):
        word = matrix.get_word(j)
        V, A, B = extract_fields(word)
        v_str = ''.join(map(str, V))
        a_str = ''.join(map(str, A))
        b_str = ''.join(map(str, B))
        v_int = int(v_str, 2)
        a_int = int(a_str, 2)
        b_int = int(b_str, 2)
        print(f"Слово {j:2}: V={v_int} ({v_str}), A={a_int} ({a_str}), B={b_int} ({b_str})")