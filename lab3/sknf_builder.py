class SKNFBuilder:
    def __init__(self, truth_table, letters_list):
        self.truth_table = truth_table
        self.letters_list = letters_list

    def build_sknf(self):
        sknf = []
        for i in range(1, len(self.truth_table[0])):
            if self.truth_table[-1][i] == "0":
                term = []
                for j in range(len(self.letters_list)):
                    if self.truth_table[j][i] == "1":
                        term.append(f"!{self.letters_list[j]}")
                    else:
                        term.append(self.letters_list[j])
                    term.append("|")
                term.pop()  # Remove last '|'
                sknf.append("(" + "".join(term) + ")")
                sknf.append("&")
        if sknf:
            sknf.pop()  # Remove last '&'
        return "".join(sknf) if sknf else "1"

    def get_maxterms(self):
        n = len(self.letters_list)
        maxterms = []
        for i in range(1, len(self.truth_table[0])):
            if self.truth_table[-1][i] == "0":
                maxterm = [int(self.truth_table[j][i]) for j in range(n)]
                maxterms.append(maxterm)
        return maxterms