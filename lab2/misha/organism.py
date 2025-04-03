import random
import pygame
from typing import List, Optional

# Инициализация Pygame
pygame.init()


class CultureMediumCell:
    def __init__(self):
        self.animal = None
        self.new_animal = None

    def NewEra(self):
        self.new_animal = None


class CultureMediumAnimal:
    def ToAlive(self, cell: CultureMediumCell) -> None:
        pass

    def ToEat(self, cell: CultureMediumCell) -> None:
        pass

    def ToJump(self, from_cell: CultureMediumCell, to_cell: CultureMediumCell) -> None:
        to_cell.new_animal = self
        from_cell.animal = None


class CultureMedium1:
    def __init__(self, distribution_ratio: float, size: int, cell_size: int = 20):
        self._rand = random.Random()
        self.size = size
        self.cell_size = cell_size  # Размер клетки в пикселях
        self.distribution_ratio = distribution_ratio
        self.generation = self._get_zero_generation(distribution_ratio, size)

        # Настройка окна Pygame
        self.screen = pygame.display.set_mode((size * cell_size, size * cell_size))
        pygame.display.set_caption("Culture Medium Simulation")
        self.clock = pygame.time.Clock()

    def _get_zero_generation(self, distribution_ratio: float, size: int) -> List[List[CultureMediumCell]]:
        generation = [[CultureMediumCell() for _ in range(size)] for _ in range(size)]

        amount_cell = int(round(size * size * distribution_ratio))
        values = random.sample(range(size * size), amount_cell)

        for value in values:
            i, j = divmod(value, size)
            generation[i][j].animal = CultureMediumAnimal()

        return generation

    def update_generation(self) -> None:
        for i in range(self.size):
            for j in range(self.size):
                self.generation[i][j].NewEra()

        self._jump_cell(self.generation[0][0],
                        [self.generation[0][1],
                         self.generation[1][0],
                         self.generation[1][1]])

        self._jump_cell(self.generation[self.size - 1][0],
                        [self.generation[self.size - 1][1],
                         self.generation[self.size - 2][0],
                         self.generation[self.size - 2][1]])

        self._jump_cell(self.generation[0][self.size - 1],
                        [self.generation[0][self.size - 2],
                         self.generation[1][self.size - 2],
                         self.generation[1][self.size - 1]])

        self._jump_cell(self.generation[self.size - 1][self.size - 1],
                        [self.generation[self.size - 2][self.size - 2],
                         self.generation[self.size - 1][self.size - 2],
                         self.generation[self.size - 2][self.size - 1]])

        for i in range(1, self.size - 1):
            self._jump_cell(self.generation[0][i],
                            [self.generation[0][i - 1],
                             self.generation[0][i + 1],
                             self.generation[1][i - 1],
                             self.generation[1][i],
                             self.generation[1][i + 1]])

            self._jump_cell(self.generation[self.size - 1][i],
                            [self.generation[self.size - 1][i - 1],
                             self.generation[self.size - 1][i + 1],
                             self.generation[self.size - 2][i],
                             self.generation[self.size - 2][i - 1],
                             self.generation[self.size - 2][i + 1]])

            self._jump_cell(self.generation[i][0],
                            [self.generation[i - 1][0],
                             self.generation[i + 1][0],
                             self.generation[i][1],
                             self.generation[i - 1][1],
                             self.generation[i + 1][1]])

            self._jump_cell(self.generation[i][self.size - 1],
                            [self.generation[i - 1][self.size - 1],
                             self.generation[i + 1][self.size - 1],
                             self.generation[i][self.size - 2],
                             self.generation[i - 1][self.size - 2],
                             self.generation[i + 1][self.size - 2]])

        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                self._jump_cell(self.generation[i][j],
                                [self.generation[i - 1][j],
                                 self.generation[i + 1][j],
                                 self.generation[i][j - 1],
                                 self.generation[i - 1][j - 1],
                                 self.generation[i + 1][j - 1],
                                 self.generation[i][j + 1],
                                 self.generation[i - 1][j + 1],
                                 self.generation[i + 1][j + 1]])

    def _jump_cell(self, current_cell: CultureMediumCell, cells: List[CultureMediumCell]) -> None:
        if current_cell.animal is not None:
            current_cell.animal.ToAlive(current_cell)
            if current_cell.animal is not None:
                current_cell.animal.ToEat(current_cell)

                empty_cells = [cell for cell in cells if cell.animal is None]
                if empty_cells:
                    target_cell = random.choice(empty_cells)
                    current_cell.animal.ToJump(current_cell, target_cell)

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))  # Белый фон

        for i in range(self.size):
            for j in range(self.size):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                   self.cell_size, self.cell_size)
                # Рисуем сетку
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

                # Рисуем животное, если оно есть
                if self.generation[i][j].animal is not None:
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     (j * self.cell_size + 2, i * self.cell_size + 2,
                                      self.cell_size - 4, self.cell_size - 4))

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Обновление по нажатию пробела
                        self.update_generation()

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()


if __name__ == "__main__":
    medium = CultureMedium1(distribution_ratio=0.3, size=20, cell_size=20)
    medium.run()