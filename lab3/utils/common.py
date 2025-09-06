from typing import List, Tuple

def term_to_string(term: List[Tuple[str, int]], is_sknf: bool = False) -> str:
    """Преобразует терм в строку. Для СКНФ использует |, для СДНФ — &."""
    parts = []
    for var, val in term:
        if val is None:
            continue
        if is_sknf:
            if val == 0:
                parts.append(var)
            else:
                parts.append(f"!{var}")
        else:
            if val == 0:
                parts.append(f"!{var}")
            else:
                parts.append(var)
    joiner = " | " if is_sknf else " & "
    return joiner.join(parts) if parts else ("1" if is_sknf else "0")