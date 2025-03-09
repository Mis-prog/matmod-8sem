import random
import numpy as np
import time
import os
import pygame
import sys


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

if not os.path.exists("result/frames_gamelife"):
    os.makedirs("result/frames_gamelife")


def main():
    frame_count = 0
    CELL_SIZE = 15  # Размер клетки в пикселях
    GRID_COLOR = (50, 50, 50)  # Цвет сетки
    ALIVE_COLOR = (255, 255, 255)  # Цвет живых клеток
    DEAD_COLOR = (0, 0, 0)  # Цвет мертвых клеток
    BACKGROUND_COLOR = (10, 10, 10)
    FPS = 10

    size = 32
    distribution_ratio = 0.3

    width = size * CELL_SIZE
    height = size * CELL_SIZE

    # Инициализация pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Игра 'Жизнь'")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Создаем игру
    game = GameLife(distribution_ratio, size)

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
                    game = GameLife(distribution_ratio, size)
                    generation_count = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Инвертирование клетки при клике
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if 0 <= grid_x < size and 0 <= grid_y < size:
                    game.generation[grid_y, grid_x] = 1 - game.generation[grid_y, grid_x]

        # Обновление поколения, если игра не на паузе
        if not paused:
            game.update_generation()
            generation_count += 1

        # Очистка экрана
        screen.fill(BACKGROUND_COLOR)

        # Отрисовка клеток
        for y in range(size):
            for x in range(size):
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                # Рисуем клетку
                cell_color = ALIVE_COLOR if game.generation[y, x] == 1 else DEAD_COLOR
                pygame.draw.rect(screen, cell_color, cell_rect)

                # Рисуем границу клетки
                pygame.draw.rect(screen, GRID_COLOR, cell_rect, 1)

        # Получаем статистику
        _, active_cells, passive_cells, dead_cells = game.current_generation_to_string()

        # Отображаем информацию
        info_text = f"Поколение: {generation_count} | Живые: {active_cells} | Мертвые: {dead_cells}"
        # info_text += " | [ПАУЗА]" if paused else ""
        # info_text += " | ПРОБЕЛ: пауза | R: рестарт | ESC: выход | КЛИК: изменить клетку"

        # Отображаем информацию в заголовке окна
        pygame.display.set_caption(info_text)

        # Обновляем экран
        pygame.display.flip()

        pygame.image.save(screen, f"result/frames_gamelife/frame_{frame_count}.png")
        frame_count += 1
        # Ограничиваем FPS
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
