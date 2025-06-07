from utils import differ_by_one_string, glue_implicants_string, covers_minterm

def minimize_dnf_calc(dnf: list[str], variables: list[str]) -> str:
    """
    Расчетный метод минимизации СДНФ с удалением лишних импликант.
    :param dnf: список строковых импликант ['!a & !b & c', 'a & !b & !c', ...]
    :param variables: список переменных ['a', 'b', 'c']
    :return: минимизированная форма в виде строки с импликантами в скобках
    """
    if not dnf:
        return "0"

    # Инициализация
    prime_implicants = []  # (импликанта, стадия)
    glued_pairs = []  # Этапы склеивания
    current_implicants = dnf.copy()
    stage = 0

    # Этап склеивания
    while current_implicants:
        next_implicants = []
        used = set()

        # Проверяем все пары для склеивания
        for i in range(len(current_implicants)):
            for j in range(i + 1, len(current_implicants)):
                imp1, imp2 = current_implicants[i], current_implicants[j]
                can_glue, diff_index = differ_by_one_string(imp1, imp2, variables)
                if can_glue:
                    new_imp = glue_implicants_string(imp1, diff_index, variables)
                    if new_imp and new_imp not in next_implicants:
                        next_implicants.append(new_imp)
                        used.add(i)
                        used.add(j)
                        glued_pairs.append(f"({imp1}) ∨ ({imp2}) => ({new_imp})")

        # Добавляем несклеенные импликанты как простые
        for i in range(len(current_implicants)):
            if i not in used and current_implicants[i] not in [imp for imp, _ in prime_implicants]:
                prime_implicants.append((current_implicants[i], stage))

        if not next_implicants:
            break

        current_implicants = next_implicants
        stage += 1

    # Удаление лишних импликант
    original_minterms = dnf.copy()
    essential_implicants = []
    covered_minterms = set()

    # Находим существенные импликанты
    for imp, stage in prime_implicants:
        # Проверяем, покрывает ли импликанта минтермы, не покрываемые другими
        covered = {m for m in original_minterms if covers_minterm(imp, m)}
        if not covered:
            continue
        is_essential = False
        for m in covered:
            other_covered = sum(1 for other_imp, _ in prime_implicants
                                if other_imp != imp and covers_minterm(other_imp, m))
            if other_covered == 0:
                is_essential = True
                break
        if is_essential and (imp, stage) not in essential_implicants:
            essential_implicants.append((imp, stage))
            covered_minterms.update(covered)

    # Покрываем оставшиеся минтермы
    remaining_minterms = [m for m in original_minterms if m not in covered_minterms]
    if remaining_minterms:
        # Сортируем по: стадия (позже лучше), число переменных (меньше лучше)
        non_essential = [(imp, stage) for imp, stage in prime_implicants if (imp, stage) not in essential_implicants]
        non_essential.sort(key=lambda x: (x[1], -len(x[0].split('&'))), reverse=True)

        # Жадный выбор импликант
        while remaining_minterms:
            best_imp = None
            best_coverage = set()
            best_score = (-1, 0, 0)  # (стадия, покрытие, -число переменных)

            for imp, stage in non_essential:
                covered = {m for m in remaining_minterms if covers_minterm(imp, m)}
                if covered:
                    num_vars = len(imp.split('&')) if '&' in imp else 1
                    score = (stage, len(covered), -num_vars)
                    if score > best_score:
                        best_score = score
                        best_imp = imp
                        best_coverage = covered

            if not best_imp:
                break

            essential_implicants.append((best_imp, stage))
            covered_minterms.update(best_coverage)
            remaining_minterms = [m for m in remaining_minterms if m not in covered_minterms]
            non_essential = [(imp, s) for imp, s in non_essential if imp != best_imp]

    # Извлекаем импликанты и удаляем дубликаты
    final_implicants = list(dict.fromkeys(imp for imp, _ in essential_implicants))

    # Вывод этапов склеивания
    print("Этапы склеивания:")
    for pair in glued_pairs:
        print(pair)

    # Формируем финальную строку
    final_result = " ∨ ".join(f"({imp})" for imp in final_implicants) if final_implicants else "0"
    return final_result