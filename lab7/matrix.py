import random

class Matrix:
    def __init__(self, random_fill=True):
        self.size = 16
        if random_fill:
            self.matrix = [[random.randint(0, 1) for _ in range(self.size)] for _ in range(self.size)]
        else:
            self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def get_word(self, j):
        return [self.matrix[i][(j + i) % self.size] for i in range(self.size)]

    def set_word(self, j, word):
        for i in range(self.size):
            self.matrix[i][(j + i) % self.size] = word[i]

    def get_column(self, k):
        return [self.matrix[k][i] for i in range(self.size)]

    def print_matrix(self):
        for row in self.matrix:
            print(" ".join(map(str, row)))