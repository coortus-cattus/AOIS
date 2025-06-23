class TruthTable:
    def __init__(self, letters_list):
        self.letters_list = letters_list
        self.truth_table = self._initialize_table()

    def _initialize_table(self):
        table = []
        n = len(self.letters_list)
        for i in range(n):
            row = [0] * (pow(2, n) + 1)
            row[0] = self.letters_list[i]
            table.append(row)
        return table

    def fill_table(self):
        n = len(self.letters_list)
        for i in range(pow(2, n)):
            binary_value = self._get_binary_value(i, n)
            for j in range(n):
                self.truth_table[j][i + 1] = binary_value[j]

    def _get_binary_value(self, value, length) -> str:
        direct_binary = ""
        abs_value = abs(value)
        while abs_value > 0:
            direct_binary = str(abs_value % 2) + direct_binary
            abs_value //= 2
        return direct_binary.zfill(length)

    def print_table(self, additional_rows=None):
        if additional_rows:
            table = self.truth_table + additional_rows
        else:
            table = self.truth_table

        header = table[0][0]
        for row in table[1:]:
            header += " " + row[0]
        print(header)

        for i in range(1, len(table[0])):
            row_values = ""
            for row in table:
                row_values += str(row[i]) + " "
            print(row_values.rstrip())
    def get_last_column(self, additional_rows=None):
        
        if additional_rows:
            table = self.truth_table + additional_rows
        else:
            table = self.truth_table

        last_column = table[-1]#[row[-1] for row in table]
        return last_column