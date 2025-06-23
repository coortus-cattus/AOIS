class SDNFBuilder:
    def __init__(self, truth_table, letters_list):
        self.truth_table = truth_table
        self.letters_list = letters_list

    def build_sdnf(self):
        sdnf = []
        for i in range(1, len(self.truth_table[0])):
            if self.truth_table[-1][i] == "1":
                term = []
                for j in range(len(self.letters_list)):
                    if self.truth_table[j][i] == "0":
                        term.append(f"!{self.letters_list[j]}")
                    else:
                        term.append(self.letters_list[j])
                    term.append("&")
                term.pop()  # Remove last '&'
                sdnf.append("(" + "".join(term) + ")")
                sdnf.append("|")
        if sdnf:
            sdnf.pop()  # Remove last '|'
        return "".join(sdnf) if sdnf else "0"
    
    def get_minterms(self):
        n = len(self.letters_list)
        minterms = []
        for i in range(1, len(self.truth_table[0])):
            if self.truth_table[-1][i] == "1":
                minterm = [int(self.truth_table[j][i]) for j in range(n)]
                minterms.append(minterm)
        return minterms