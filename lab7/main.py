from matrix import Matrix
from logical_ops import print_logic_table
from arithmetic import extract_fields, add_fields, print_words_info
from search import find_words_by_V, print_search_results

def main():
    print("=" * 50)
    print("Матрица 16x16 со случайным заполнением и диагональной адресацией")
    print("=" * 50)
    
    matrix = Matrix(random_fill=True)
    print("\nМатрица 16x16 (случайное заполнение):")
    matrix.print_matrix()
    
    print("\n" + "=" * 50)
    print_words_info(matrix)
    
    print("\n" + "=" * 50)
    print("Тестирование логических функций:")
    print_logic_table()
    
    print("\n" + "=" * 50)
    V_key = [1, 0, 1]  # Пример: V=5 (101)
    v_key_str = ''.join(map(str, V_key))
    v_key_int = int(v_key_str, 2)
    print(f"Поиск слова с V={v_key_int} ({v_key_str}):")
    print_search_results(matrix, V_key)
    
    print("\n" + "=" * 50)
    target_V = [0, 1, 1]  # Пример: V=3 (011)
    target_str = ''.join(map(str, target_V))
    target_int = int(target_str, 2)
    print(f"Сложение A и B для слов с V={target_int} ({target_str}):")
    found_words = find_words_by_V(matrix, target_V)
    if found_words:
        for j in found_words:
            word = matrix.get_word(j)
            V, A, B = extract_fields(word)
            a_str = ''.join(map(str, A))
            b_str = ''.join(map(str, B))
            a_int = int(a_str, 2)
            b_int = int(b_str, 2)
            sum_ab = add_fields(A, B)
            print(f"Слово {j:2}: A={a_int} ({a_str}) + B={b_int} ({b_str}) = {sum_ab}")
    else:
        print("Слова с заданным V не найдены")

if __name__ == "__main__":
    main()