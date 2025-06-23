class Minimizer:
    def __init__(self, letters_list, truth_table):
        self.letters_list = letters_list
        self.truth_table = truth_table
        self.n = len(letters_list)

    def _minimize_common(self, terms, is_sdnf):
        if not terms:
            return "Function is always true" if is_sdnf else "Function is always false"

        current_terms = terms
        step = 1
        # for term in current_terms:
        #     print("".join(str(x) for x in term))

        while True:
            combined_set = set()
            new_terms_set = set()

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term1, term2 = current_terms[i], current_terms[j]
                    diff = 0
                    diff_pos = -1
                    for k in range(self.n):
                        if term1[k] != term2[k]:
                            diff += 1
                            diff_pos = k
                    if diff == 1:
                        new_term = term1.copy()
                        new_term[diff_pos] = "X"
                        new_terms_set.add(tuple(new_term))
                        combined_set.add(i)
                        combined_set.add(j)

            if new_terms_set:
                # print("Combined implicants:")
                for term in new_terms_set:
                    print("".join(str(x) for x in term))
            else:
                print("No more combinations possible")
                break

            result_set = set(new_terms_set)
            for i in range(len(current_terms)):
                if i not in combined_set:
                    result_set.add(tuple(current_terms[i]))
            current_terms = [list(term) for term in result_set]
            step += 1

        return current_terms

    def minimize_sdnf_raschetny(self, minterms):
        current_terms = self._minimize_common(minterms, True)
        print("\nMinimized SDNF:")
        result_expr = []
        for term in current_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == "X":
                    continue
                term_str.append(
                    f"!{self.letters_list[i]}" if term[i] == 0 else self.letters_list[i]
                )
            if term_str:
                result_expr.append("(" + "&".join(term_str) + ")")
        final_expr = "|".join(result_expr) if result_expr else "0"
        print(final_expr)
        self.result_final_expr = final_expr
        return final_expr

    def minimize_sknf_raschetny(self, maxterms):
        current_terms = self._minimize_common(maxterms, False)
        print("\nMinimized SKNF:")
        sknf_result_expr = []
        for term in current_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == "X":
                    continue
                term_str.append(
                    self.letters_list[i] if term[i] == 0 else f"!{self.letters_list[i]}"
                )
            if term_str:
                sknf_result_expr.append("(" + "|".join(term_str) + ")")
        final_expr = "&".join(sknf_result_expr) if sknf_result_expr else "1"
        self.result_sf=final_expr 
        print(final_expr)
        return final_expr

    def _build_coverage_table(self, terms, original_terms):
        table = []
        for term in terms:
            row = []
            for minterm in original_terms:
                is_covered = all(
                    term[i] == "X" or term[i] == minterm[i] for i in range(self.n)
                )
                row.append(1 if is_covered else 0)
            table.append(row)
        return table

    def minimize_sdnf_raschet_table(self, minterms):
        if not minterms:
            return "Function is always true"
        current_terms = self._minimize_common(minterms, True)
        print("\nCombined terms:")
        print(current_terms)

        table = self._build_coverage_table(current_terms, minterms)
        print("\nCoverage table:")
        col_width = max(4, max(len("".join(str(x) for x in term)) for term in minterms))
        header = ["".join(str(x) for x in term) for term in minterms]
        separator = "-" * col_width + "+" + "+".join("-" * col_width for _ in header) + "+"
        header_line = " " * col_width + "|" + "|".join(f"{h:^{col_width}}" for h in header) + "|"
        print(separator)
        print(header_line)
        print(separator)

        for i, row in enumerate(table):
            term_str = "".join(str(x) for x in current_terms[i])
            print(f"{term_str:<{col_width}}|" + "|".join(f"{x:^{col_width}}" for x in row) + "|")
        print(separator)

        result_terms = set()
        for j in range(len(minterms)):
            one_count = 0
            term_idx = -1
            for i in range(len(current_terms)):
                if table[i][j] == 1:
                    one_count += 1
                    term_idx = i
            if one_count == 1:
                result_terms.add(tuple(current_terms[term_idx]))

        print("\nEssential implicants:", result_terms)
        print("\nMinimized SDNF:")
        result_expr = []
        for term in result_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == "X":
                    continue
                term_str.append(
                    f"!{self.letters_list[i]}" if term[i] == 0 else self.letters_list[i]
                )
            if term_str:
                result_expr.append("(" + "&".join(term_str) + ")")
        final_expr = "|".join(result_expr) if result_expr else "0"
        print(final_expr)
        return final_expr

    def minimize_sknf_raschet_table(self, maxterms):
        if not maxterms:
            return "Function is always true"
        current_terms = self._minimize_common(maxterms, False)
        print("\nCombined terms:")
        print(current_terms)

        table = self._build_coverage_table(current_terms, maxterms)
        print("\nCoverage table:")
        col_width = max(4, max(len("".join(str(x) for x in term)) for term in maxterms))
        header = ["".join(str(x) for x in term) for term in maxterms]
        separator = "-" * col_width + "+" + "+".join("-" * col_width for _ in header) + "+"
        header_line = " " * col_width + "|" + "|".join(f"{h:^{col_width}}" for h in header) + "|"
        print(separator)
        print(header_line)
        print(separator)

        for i, row in enumerate(table):
            term_str = "".join(str(x) for x in current_terms[i])
            print(f"{term_str:<{col_width}}|" + "|".join(f"{x:^{col_width}}" for x in row) + "|")
        print(separator)

        result_terms = set()
        for j in range(len(maxterms)):
            one_count = 0
            term_idx = -1
            for i in range(len(current_terms)):
                if table[i][j] == 1:
                    one_count += 1
                    term_idx = i
            if one_count == 1:
                result_terms.add(tuple(current_terms[term_idx]))

        print("\nEssential implicants:", result_terms)
        print("\nMinimized SKNF:")
        result_expr = []
        for term in result_terms:
            term_str = []
            for i in range(len(term)):
                if term[i] == "X":
                    continue
                term_str.append(
                    self.letters_list[i] if term[i] == 0 else f"!{self.letters_list[i]}"
                )
            if term_str:
                result_expr.append("(" + "|".join(term_str) + ")")
        final_expr = "&".join(result_expr) if result_expr else "1"
        print(final_expr)
        return final_expr

    def _setup_karnaugh_map(self, terms, is_sdnf):
        if not terms:
            print(f"Function is {'1' if is_sdnf else '0'}, no {'minterms' if is_sdnf else 'maxterms'}")
            return None, None, None, None, None

        if self.n > 5:
            print("Karnaugh map supports only 2-5 variables")
            return None, None, None, None, None

        if self.n == 2:
            rows, cols = 2, 2
            row_vars = [self.letters_list[0]]
            col_vars = [self.letters_list[1]]
        elif self.n == 3:
            rows, cols = 2, 4
            row_vars = [self.letters_list[0]]
            col_vars = [self.letters_list[1], self.letters_list[2]]
        elif self.n == 4:
            rows, cols = 4, 4
            row_vars = [self.letters_list[0], self.letters_list[1]]
            col_vars = [self.letters_list[2], self.letters_list[3]]
        else:
            rows, cols = 4, 8
            row_vars = [self.letters_list[0], self.letters_list[1]]
            col_vars = [self.letters_list[2], self.letters_list[3], self.letters_list[4]]

        kmap = [[1 if not is_sdnf else 0] * cols for _ in range(rows)]
        gray_rows = ["0", "1"] if rows == 2 else ["00", "01", "11", "10"]
        gray_cols = (
            ["0", "1"] if cols == 2
            else ["00", "01", "11", "10"] if cols == 4
            else ["000", "001", "011", "010", "110", "111", "101", "100"]
        )

        for term in terms:
            if self.n == 2:
                row, col = term[0], term[1]
            elif self.n == 3:
                row = term[0]
                col_bin = "".join(str(term[i]) for i in [1, 2])
                col = {"00": 0, "01": 1, "11": 2, "10": 3}[col_bin]
            elif self.n == 4:
                row_bin = "".join(str(term[i]) for i in [0, 1])
                col_bin = "".join(str(term[i]) for i in [2, 3])
                row = {"00": 0, "01": 1, "11": 2, "10": 3}[row_bin]
                col = {"00": 0, "01": 1, "11": 2, "10": 3}[col_bin]
            else:
                row_bin = "".join(str(term[i]) for i in [0, 1])
                col_bin = "".join(str(term[i]) for i in [2, 3, 4])
                row = {"00": 0, "01": 1, "11": 2, "10": 3}[row_bin]
                col = {
                    "000": 0, "001": 1, "011": 2, "010": 3,
                    "110": 4, "111": 5, "101": 6, "100": 7
                }[col_bin]
            kmap[row][col] = 1 if is_sdnf else 0

        return kmap, rows, cols, row_vars, col_vars, gray_rows, gray_cols

    def karnaugh_map_sdnf(self, minterms):
        kmap, rows, cols, row_vars, col_vars, gray_rows, gray_cols = self._setup_karnaugh_map(minterms, True)
        if kmap is None:
            return "0"

        print("\Карта Карно для SDNF:")
        header = (
            f"{'':4} {col_vars[0]}=0 {col_vars[0]}=1" if self.n == 2
            else f"{'':4} {col_vars[0]}{col_vars[1]}=00 {col_vars[0]}{col_vars[1]}=01 {col_vars[0]}{col_vars[1]}=11 {col_vars[0]}{col_vars[1]}=10" if self.n <= 4
            else f"{'':4} {col_vars[0]}{col_vars[1]}{col_vars[2]}=000 {col_vars[0]}{col_vars[1]}{col_vars[2]}=001 {col_vars[0]}{col_vars[2]}=011 {col_vars[0]}{col_vars[2]}=010 {col_vars[0]}{col_vars[2]}=110 {col_vars[0]}{col_vars[2]}=111 {col_vars[0]}{col_vars[2]}=101 {col_vars[0]}{col_vars[2]}=100"
        )
        print(header)
        for i in range(rows):
            row_label = (
                f"{row_vars[0]}={gray_rows[i]}" if self.n <= 3
                else f"{row_vars[0]}{row_vars[1]}={gray_rows[i]}"
            )
            print(f"{row_label:4} {' '.join(str(kmap[i][j]) for j in range(cols))}")

        # Находим все возможные группы единиц
        groups = []
        covered = set()
        target = 1  # Для СДНФ ищем единицы
        possible_sizes = [8, 4, 2, 1] if self.n > 2 else [4, 2, 1]
        for size in possible_sizes:
            if size > rows * cols:
                continue
            for h in [1, 2, 4] if size > 1 else [1]:
                for w in [size // h] if h * (size // h) == size else []:
                    for r in range(rows):
                        for c in range(cols):
                            cells = set()
                            valid = True
                            for i in range(h):
                                for j in range(w):
                                    i_mod = (r + i) % rows
                                    j_mod = (c + j) % cols
                                    if kmap[i_mod][j_mod] != target:
                                        valid = False
                                        break
                                    cells.add((i_mod, j_mod))
                                if not valid:
                                    break
                            if valid and cells and len(cells) == size:
                                if cells - covered:  # Добавляем, если покрывает новые клетки
                                    groups.append(cells)
                                    covered.update(cells)

        # Формируем импликанты из групп
        result = []
        for group in groups:
            term = []
            for var_idx in range(self.n):
                var = self.letters_list[var_idx]
                values = set()
                for r, c in group:
                    if self.n == 2:
                        bin_str = f"{r}{c}"
                    elif self.n == 3:
                        bin_str = f"{r}{gray_cols[c]}"
                    elif self.n == 4:
                        bin_str = f"{gray_rows[r]}{gray_cols[c]}"
                    else:
                        bin_str = f"{gray_rows[r]}{gray_cols[c]}"
                    values.add(int(bin_str[var_idx]))
                if len(values) == 1:
                    val = values.pop()
                    term.append(f"{var}" if val == 1 else f"!{var}")
            if term:
                result.append("(" + "&".join(term) + ")")

        final_expr = "|".join(result) if result else "0"
        print("\Минимизированная SDNF (Карта Карно):")
        print(final_expr)
        return final_expr

    def karnaugh_map_sknf(self, maxterms):
        kmap, rows, cols, row_vars, col_vars, gray_rows, gray_cols = self._setup_karnaugh_map(maxterms, False)
        if kmap is None:
            return "1"

        print("\Карта Карно для SKNF:")
        header = (
            f"{'':4} {col_vars[0]}=0 {col_vars[0]}=1" if self.n == 2
            else f"{'':4} {col_vars[0]}{col_vars[1]}=00 {col_vars[0]}{col_vars[1]}=01 {col_vars[0]}{col_vars[1]}=11 {col_vars[0]}{col_vars[1]}=10" if self.n <= 4
            else f"{'':4} {col_vars[0]}{col_vars[1]}{col_vars[2]}=000 {col_vars[0]}{col_vars[1]}{col_vars[2]}=001 {col_vars[0]}{col_vars[1]}{col_vars[2]}=011 {col_vars[0]}{col_vars[1]}{col_vars[2]}=010 {col_vars[0]}{col_vars[1]}{col_vars[2]}=110 {col_vars[0]}{col_vars[1]}{col_vars[2]}=111 {col_vars[0]}{col_vars[1]}{col_vars[2]}=101 {col_vars[0]}{col_vars[1]}{col_vars[2]}=100"
        )
        print(header)
        for i in range(rows):
            row_label = (
                f"{row_vars[0]}={gray_rows[i]}" if self.n <= 3
                else f"{row_vars[0]}{row_vars[1]}={gray_rows[i]}"
            )
            print(f"{row_label:4} {' '.join(str(kmap[i][j]) for j in range(cols))}")

        # Находим все возможные группы нулей
        groups = []
        covered = set()
        target = 0  # Для СКНФ ищем нули
        possible_sizes = [8, 4, 2, 1] if self.n > 2 else [4, 2, 1]
        for size in possible_sizes:
            if size > rows * cols:
                continue
            for h in [1, 2, 4] if size > 1 else [1]:
                for w in [size // h] if h * (size // h) == size else []:
                    for r in range(rows):
                        for c in range(cols):
                            cells = set()
                            valid = True
                            for i in range(h):
                                for j in range(w):
                                    i_mod = (r + i) % rows
                                    j_mod = (c + j) % cols
                                    if kmap[i_mod][j_mod] != target:
                                        valid = False
                                        break
                                    cells.add((i_mod, j_mod))
                                if not valid:
                                    break
                            if valid and cells and len(cells) == size:
                                if cells - covered:  # Добавляем, если покрывает новые клетки
                                    groups.append(cells)
                                    covered.update(cells)

        # Формируем импликанты из групп
        result = []
        for group in groups:
            term = []
            for var_idx in range(self.n):
                var = self.letters_list[var_idx]
                values = set()
                for r, c in group:
                    if self.n == 2:
                        bin_str = f"{r}{c}"
                    elif self.n == 3:
                        bin_str = f"{r}{gray_cols[c]}"
                    elif self.n == 4:
                        bin_str = f"{gray_rows[r]}{gray_cols[c]}"
                    else:
                        bin_str = f"{gray_rows[r]}{gray_cols[c]}"
                    values.add(int(bin_str[var_idx]))
                if len(values) == 1:
                    val = values.pop()
                    term.append(f"{var}" if val == 0 else f"!{var}")
            if term:
                result.append("(" + "|".join(term) + ")")

        final_expr = "&".join(result) if result else "1"
        print("\Минимизированная SKNF (Карта Карно):")
        print(final_expr)
        return final_expr