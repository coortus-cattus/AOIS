class OPZConverter:
    def __init__(self, func_str, operations_array, letters_list):
        self.func_str = func_str
        self.operations_array = operations_array
        self.letters_list = letters_list
        self.opz = self._convert_to_opz()

    def _priority(self, char):
        priority_map = {">": 2, "&": 2,"/": 2, "|": 2, "~": 2, "!": 3, "(": 1}
        return priority_map.get(char, 0)

    def _convert_to_opz(self):
        stack = []
        opz = ""
        for char in self.func_str:
            if char == "(":
                stack.append(char)
            elif char == ")":
                while stack and stack[-1] != "(":
                    opz += stack.pop()
                stack.pop()  # Remove '('
            elif char in self.letters_list:
                opz += char
            elif char in self.operations_array:
                while stack and self._priority(stack[-1]) >= self._priority(char):
                    opz += stack.pop()
                stack.append(char)
        while stack:
            opz += stack.pop()
        return opz