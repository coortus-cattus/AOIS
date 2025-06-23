class LogicOperator:
  def __init__(self, func_str: str):
      self.operations_array = ["&", "D", "|", "!", "~",'/']
      self.letters_array = ["a", "b", "c", "d", "e"]
      self.func_str = func_str
      self.new_letters_list = []

      # Extract unique variables from the expression
      for char in self.func_str:
          if (
              char not in self.operations_array
              and char not in self.new_letters_list
              and char in self.letters_array
          ):
              self.new_letters_list.append(char)

      print(f"Variables in expression: {''.join(self.new_letters_list)}")