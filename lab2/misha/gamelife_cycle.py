import numpy as np
import pygame
import sys
import os
import re


def rle_to_numpy(rle_string):
    lines = rle_string.strip().splitlines()
    header = [line for line in lines if not line.startswith('#') and not line.startswith('x')][0]
    pattern_lines = [line for line in lines if not line.startswith('#') and not line.startswith('x')]
    rle_data = ''.join(pattern_lines).replace('\n', '').replace('!', '')

    # Парсим rle данные
    rle_tokens = re.findall(r'\d*[bo$]', rle_data)
    current_row = []
    result = []

    for token in rle_tokens:
        count = int(re.findall(r'\d+', token)[0]) if re.findall(r'\d+', token) else 1
        char = token[-1]

        if char == 'b':
            current_row.extend([0] * count)
        elif char == 'o':
            current_row.extend([1] * count)
        elif char == '$':
            result.append(current_row)
            current_row = []

    # Добавляем последнюю строку, если не пустая
    if current_row:
        result.append(current_row)

    # Выровняем строки по длине
    max_len = max(len(row) for row in result)
    for row in result:
        row.extend([0] * (max_len - len(row)))

    return np.array(result, dtype=int)


class GameLife2:
    def __init__(self, distribution_ratio, size):
        self.size = size
        self.distribution_ratio = distribution_ratio
        self.generation = self.get_cycle_generation(distribution_ratio, size)

    def get_cycle_generation(self, distribution_ratio, size):
        # Создаём пустое поле
        generation = np.zeros((size, size), dtype=int)

        # # Биполь (20-22 строки, 3-5 столбцы)
        generation[5, 3:6] = [0, 0, 0]
        generation[6, 3:6] = [1, 1, 1]
        generation[7, 3:6] = [0, 0, 0]

        # # Жаба (20-23 строки, 10-13 столбцы)
        generation[5, 10:14] = [0, 0, 0, 0]
        generation[6, 10:14] = [0, 1, 1, 1]
        generation[7, 10:14] = [1, 1, 1, 0]
        generation[8, 10:14] = [0, 0, 0, 0]
        #
        # # Маяк (20-23 строки, 20-23 столбцы)
        generation[5, 20:24] = [1, 1, 0, 0]
        generation[6, 20:24] = [1, 0, 0, 0]
        generation[7, 20:24] = [0, 0, 0, 1]
        generation[8, 20:24] = [0, 0, 1, 1]


        rle5_1 = '''
        x = 13, y = 12, rule = B3/S23
        2o$bo$bobo$2b2o$6b2o$6bo$6bo$5b2o$9b2o$9bobo$11bo$11b2o!
        '''

        rle5_2 = '''
        x = 16, y = 7, rule = B3/S23
        7b2o$2b2obo4bob2o$2bo10bo$3b2o6b2o$3o2b6o2b3o$o2bo8bo2bo$b2o10b2o!
        '''

        rle8 = '''
        x = 10, y = 5, rule = B3/S23
        6bobob$5bo4b$2o2bo4bo$2obo2bob2o$4b2o!
        '''


        pattern = rle_to_numpy(rle5_1)

        h, w = pattern.shape
        start_x = 5
        start_y = 30
        generation[start_x:start_x+h, start_y:start_y+w] = pattern


        pattern = rle_to_numpy(rle5_2)

        h, w = pattern.shape
        start_x = 20
        start_y = 1
        generation[start_x:start_x+h, start_y:start_y+w] = pattern

        pattern = rle_to_numpy(rle8)

        h, w = pattern.shape
        start_x = 20
        start_y = 30
        generation[start_x:start_x+h, start_y:start_y+w] = pattern
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
    ALIVE_COLOR = (0, 0, 0)
    DEAD_COLOR = (255, 255, 255)
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
