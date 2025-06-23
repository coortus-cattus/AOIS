class IndexForm:
    def __init__(self, truth_table):
        self.truth_table = truth_table

    def compute_index(self):
        result = ""
        for i in range(1, len(self.truth_table[0])):
            result += self.truth_table[-1][i]
        return self._binary_to_decimal(result)

    def _binary_to_decimal(self, value):
        result = 0
        for i, digit in enumerate(reversed(value)):
            result += int(digit) * (2 ** i)
        return result