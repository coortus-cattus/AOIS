def apply_logical_function(func, word1, word2):
    func_map = {
        "f1": lambda b1, b2: b1 and b2,
        "f14": lambda b1, b2: not (b1 or b2),
        "f3": lambda b1, b2: b1 and not b2,
        "f12": lambda b1, b2: not b1
    }
    return [int(func_map[func](b1, b2)) for b1, b2 in zip(word1, word2)]

def print_logic_table():
    print("x1 x2 | f1 f14 f3 f12")
    print("--------------------")
    for x1, x2 in [(0,0), (0,1), (1,0), (1,1)]:
        res = [
            apply_logical_function("f1", [x1], [x2])[0],
            apply_logical_function("f14", [x1], [x2])[0],
            apply_logical_function("f3", [x1], [x2])[0],
            apply_logical_function("f12", [x1], [x2])[0]
        ]
        print(f"{x1}  {x2}  | {res[0]}   {res[1]}   {res[2]}   {res[3]}")