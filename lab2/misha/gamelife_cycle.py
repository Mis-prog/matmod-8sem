
import numpy as np
import pygame
import sys
import os


class GameLife2:
    def __init__(self, distribution_ratio, size):
        self.size = size
        self.distribution_ratio = distribution_ratio
        self.generation = self.get_cycle_generation(distribution_ratio, size)

    def get_cycle_generation(self, distribution_ratio, size):
        # Создаём пустое поле
        generation = np.zeros((size, size), dtype=int)

        # Квадрат (3-8 строки, 3-8 столбцы, без диагонали)
        for i in range(3, 9):
            for j in range(3, 9):
                if i != j:
                    generation[i, j] = 1
        generation[3, 8] = 0
        generation[4, 7] = 0
        generation[5, 6] = 0
        generation[6, 5] = 0
        generation[7, 4] = 0
        generation[8, 3] = 0

        # Крест (3-10 строки, 20-27 столбцы)
        generation[3, 20:28] = [0, 0, 1, 1, 1, 1, 0, 0]
        generation[4, 20:28] = [0, 0, 1, 0, 0, 1, 0, 0]
        generation[5, 20:28] = [1, 1, 1, 0, 0, 1, 1, 1]
        generation[6, 20:28] = [1, 0, 0, 0, 0, 0, 0, 1]
        generation[7, 20:28] = [1, 0, 0, 0, 0, 0, 0, 1]
        generation[8, 20:28] = [1, 1, 1, 0, 0, 1, 1, 1]
        generation[9, 20:28] = [0, 0, 1, 0, 0, 1, 0, 0]
        generation[10, 20:28] = [0, 0, 1, 1, 1, 1, 0, 0]

        # Круги (3-15 строки, 40-52 столбцы)
        generation[3, 40:53] = [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
        generation[4, 40:53] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        generation[5, 40:53] = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        generation[6, 40:53] = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        generation[7, 40:53] = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        generation[8, 40:53] = [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
        generation[9, 40:53] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        generation[10, 40:53] = [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
        generation[11, 40:53] = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        generation[12, 40:53] = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        generation[13, 40:53] = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
        generation[14, 40:53] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        generation[15, 40:53] = [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]

        # Семафор (3 строка, 60-62 столбцы)
        generation[3, 60:63] = [1, 1, 1]

        return generation

    def update_generation(self):
        new_generation = np.zeros((self.size, self.size), dtype=int)

        # Углы
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

        # Границы (не углы)
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

        # Внутренние клетки
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
        elif current_cell == 0 and sum_cells == 3:
            return_value = 1

        return return_value

    def current_generation_to_string(self):
        active_cells = 0
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
        return '\n'.join(result), active_cells, 0, dead_cells


if not os.path.exists("result/frames_gamelife"):
    os.makedirs("result/frames_gamelife")


def main():
    frame_count = 0
    CELL_SIZE = 10  # Уменьшил размер клеток, чтобы всё уместилось
    GRID_COLOR = (50, 50, 50)
    ALIVE_COLOR = (255, 255, 255)
    DEAD_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (10, 10, 10)
    FPS = 1

    size = 64  # Увеличил размер поля, чтобы вместить все структуры
    distribution_ratio = 0.3

    width = size * CELL_SIZE
    height = size * CELL_SIZE

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Игра 'Жизнь' (GameLife2)")
    clock = pygame.time.Clock()

    game = GameLife2(distribution_ratio, size)

    running = True
    paused = False
    generation_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    game = GameLife2(distribution_ratio, size)
                    generation_count = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if 0 <= grid_x < size and 0 <= grid_y < size:
                    game.generation[grid_y, grid_x] = 1 - game.generation[grid_y, grid_x]

        if not paused:
            game.update_generation()
            generation_count += 1

        screen.fill(BACKGROUND_COLOR)

        for y in range(size):
            for x in range(size):
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell_color = ALIVE_COLOR if game.generation[y, x] == 1 else DEAD_COLOR
                pygame.draw.rect(screen, cell_color, cell_rect)
                pygame.draw.rect(screen, GRID_COLOR, cell_rect, 1)

        _, active_cells, _, dead_cells = game.current_generation_to_string()
        info_text = f"Поколение: {generation_count} | Живые: {active_cells} | Мертвые: {dead_cells}"
        pygame.display.set_caption(info_text)

        pygame.display.flip()

        # pygame.image.save(screen, f"result/frames_gamelife/frame_{frame_count}.png")
        frame_count += 1
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()