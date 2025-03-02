import random
import numpy as np


class GameLife:
    def __init__(self, distribution_ratio, size):
        self.size = size
        self.distribution_ratio = distribution_ratio
        self.generation = self.get_zero_generation(distribution_ratio, size)

    def get_zero_generation(self, distribution_ratio, size):
        rand = random.Random()
        return_matrix = np.zeros((size, size), dtype=int)

        # Рассчитываем количество живых клеток
        amount_cell = round(size * size * distribution_ratio)

        # Размещаем живые клетки случайным образом
        for i in range(amount_cell):
            value = rand.randint(0, size * size - 1)
            return_matrix[value // size, value % size] = 1

        return return_matrix

    def update_generation(self):
        new_generation = np.zeros((self.size, self.size), dtype=int)

        # Обработка углов
        new_generation[0, 0] = self.new_cell(self.generation[0, 0],
                                             self.generation[0, 1],
                                             self.generation[1, 0],
                                             self.generation[1, 1])

        new_generation[self.size - 1, 0] = self.new_cell(self.generation[self.size - 1, 0],
                                                         self.generation[self.size - 1, 1],
                                                         self.generation[self.size - 2, 0],
                                                         self.generation[self.size - 2, 1])

        new_generation[0, self.size - 1] = self.new_cell(self.generation[0, self.size - 1],
                                                         self.generation[0, self.size - 2],
                                                         self.generation[1, self.size - 2],
                                                         self.generation[1, self.size - 1])

        new_generation[self.size - 1, self.size - 1] = self.new_cell(self.generation[self.size - 1, self.size - 1],
                                                                     self.generation[self.size - 2, self.size - 2],
                                                                     self.generation[self.size - 1, self.size - 2],
                                                                     self.generation[self.size - 2, self.size - 1])

        # Обработка границ (не углов)
        for i in range(1, self.size - 1):
            new_generation[0, i] = self.new_cell(self.generation[0, i],
                                                 self.generation[0, i - 1],
                                                 self.generation[0, i + 1],
                                                 self.generation[1, i - 1],
                                                 self.generation[1, i],
                                                 self.generation[1, i + 1])

            new_generation[self.size - 1, i] = self.new_cell(self.generation[self.size - 1, i],
                                                             self.generation[self.size - 1, i - 1],
                                                             self.generation[self.size - 1, i + 1],
                                                             self.generation[self.size - 2, i],
                                                             self.generation[self.size - 2, i - 1],
                                                             self.generation[self.size - 2, i + 1])

            new_generation[i, 0] = self.new_cell(self.generation[i, 0],
                                                 self.generation[i - 1, 0],
                                                 self.generation[i + 1, 0],
                                                 self.generation[i, 1],
                                                 self.generation[i - 1, 1],
                                                 self.generation[i + 1, 1])

            new_generation[i, self.size - 1] = self.new_cell(self.generation[i, self.size - 1],
                                                             self.generation[i - 1, self.size - 1],
                                                             self.generation[i + 1, self.size - 1],
                                                             self.generation[i, self.size - 2],
                                                             self.generation[i - 1, self.size - 2],
                                                             self.generation[i + 1, self.size - 2])

        # Обработка внутренних клеток
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                new_generation[i, j] = self.new_cell(self.generation[i, j],
                                                     self.generation[i - 1, j],
                                                     self.generation[i + 1, j],
                                                     self.generation[i, j - 1],
                                                     self.generation[i - 1, j - 1],
                                                     self.generation[i + 1, j - 1],
                                                     self.generation[i, j + 1],
                                                     self.generation[i - 1, j + 1],
                                                     self.generation[i + 1, j + 1])

        self.generation = new_generation

    def new_cell(self, current_cell, *cells):
        return_value = current_cell
        sum_cells = sum(cells)

        if current_cell == 1 and (sum_cells > 3 or sum_cells < 2):
            return_value = 0

        if current_cell == 0 and sum_cells == 3:
            return_value = 1

        return return_value

    def current_generation_to_string(self):
        active_cells = 0
        passive_cells = 0
        dead_cells = 0

        result = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if self.generation[i, j] == 1:
                    row.append('O')
                    active_cells += 1
                else:
                    row.append(' ')
                    dead_cells += 1
            result.append(''.join(row))

        return '\n'.join(result), active_cells, passive_cells, dead_cells