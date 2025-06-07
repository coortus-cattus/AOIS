def convert_to_implicants(formula: str, is_dnf: bool = True) -> list[str]:
    """
    Преобразует строковый СДНФ или СКНФ в список импликант.
    :param formula: строка СДНФ (например, '(!a & !b & c) | (a & !b & !c)') или СКНФ
    :param is_dnf: True для СДНФ, False для СКНФ
    :return: список импликант (например, ['!a & !b & c', 'a & !b & !c'])
    """
    if not formula or formula in ["0", "1"]:
        return []

    formula = formula.strip()
    
    implicants = []
    current = ""
    paren_count = 0
    for char in formula:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        elif char in ['|', '&'] and paren_count == 0:
            if current and current.strip():
                implicants.append(current.strip())
                current = ""
            continue
        current += char
    
    if current and current.strip():
        implicants.append(current.strip())
    
    result = []
    for imp in implicants:
        imp = imp.strip()
        if imp.startswith('(') and imp.endswith(')'):
            imp = imp[1:-1].strip()
        result.append(imp)
    
    return result

def differ_by_one_string(imp1: str, imp2: str, variables: list[str]) -> tuple[bool, int]:
    """
    Проверяет, отличаются ли две строковые импликанты ровно одной переменной.
    :param imp1: первая импликанта (например, '!a & !b & c')
    :param imp2: вторая импликанта (например, '!a & !b & !c')
    :param variables: список переменных ['a', 'b', 'c']
    :return: (bool, int) - отличаются ли и индекс различающейся переменной
    """
    parts1 = [p.strip() for p in imp1.split('&')]
    parts2 = [p.strip() for p in imp2.split('&')]
    
    # Создаем словари для переменных и их значений (True для !var, False для var)
    dict1 = {p[1:] if p.startswith('!') else p: p.startswith('!') for p in parts1}
    dict2 = {p[1:] if p.startswith('!') else p: p.startswith('!') for p in parts2}
    
    differences = 0
    diff_index = -1
    for i, var in enumerate(variables):
        # Проверяем, есть ли переменная в обеих импликантах
        val1 = dict1.get(var, None)
        val2 = dict2.get(var, None)
        if val1 is None or val2 is None:
            # Если переменная отсутствует в одной из импликант, это не склейка
            return False, -1
        if val1 != val2:
            differences += 1
            diff_index = i
        if differences > 1:
            return False, -1
    
    return differences == 1, diff_index

def glue_implicants_string(imp1: str, diff_index: int, variables: list[str]) -> str:
    """
    Склеивает две строковые импликанты, исключая различающуюся переменную.
    :param imp1: первая импликанта (например, '!a & !b & c')
    :param diff_index: индекс различающейся переменной
    :param variables: список переменных ['a', 'b', 'c']
    :return: склеенная импликанта (например, '!a & !b')
    """
    parts = [p.strip() for p in imp1.split('&')]
    result = [p for p in parts if not (p == variables[diff_index] or p == f"!{variables[diff_index]}")]
    return " & ".join(result) if result else ""

def covers_minterm(implicant: str, minterm: str) -> bool:
    """
    Проверяет, покрывает ли импликанта заданный минтерм.
    :param implicant: импликанта (например, 'a & !b')
    :param minterm: минтерм (например, 'a & !b & c')
    :return: True, если импликанта покрывает минтерм
    """
    if not implicant:
        return False
    imp_parts = {p.strip() for p in implicant.split('&')}
    min_parts = {p.strip() for p in minterm.split('&')}
    return imp_parts.issubset(min_parts)