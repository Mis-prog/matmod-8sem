import pygame
import sys
import math
import random
from copy import deepcopy

# Константы из оригинального кода
pmax = 10
r = 1
dp = 5
p1 = 35
de = 2
L = 15
dr = 3
A = 0.3
T = 3

class CellularAutomaton:
    def __init__(self, width, height, N=256):
        pygame.init()
        self.count = 0
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pygame Cellular Automaton")
        self.clock = pygame.time.Clock()

        self.N = N
        self.cell_size = min(width, height) // N

        # Цвета
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)

        # Шрифт для отображения информации
        self.font = pygame.font.SysFont('Arial', 16, True)

        # Инициализация состояний клеток
        self.cells_state = [[0] * self.N for i in range(self.N)]
        self.p = [[pmax] * self.N for i in range(self.N)]
        self.e = [[0] * self.N for i in range(self.N)]
        self.life = [[0] * self.N for i in range(self.N)]

        # Инициализация случайных живых клеток
        for i in range(int(A * N * N)):
            self.cells_state[random.randint(0, int((self.N - 1) * 0.7))][random.randint(0, self.N - 1)] = 1

    def action(self):
        # Ресурсы и энергия
        for i in range(self.N):
            for j in range(self.N):
                if self.p[i][j] != pmax:
                    self.p[i][j] += r
                self.p[i][j] = min(pmax, self.p[i][j])
                if self.cells_state[i][j] == 1:
                    if self.p[i][j] >= dp:
                        self.p[i][j] -= dp
                        self.e[i][j] += dp
                        self.e[i][j] = min(p1, self.e[i][j])
                    self.e[i][j] -= de
                    self.life[i][j] += 1

                    if self.life[i][j] > L or self.e[i][j] <= 0:
                        self.cells_state[i][j] = 0
                        self.e[i][j] = 0
                        self.life[i][j] = 0

        # Случайное движение клеток
        move = [[1] * self.N for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j] == 1 and move[i][j] == 1:
                    si = random.randint(-1, 1)
                    sj = random.randint(-1, 1)
                    if si == 0 and sj == 0:
                        si = 1
                    if i + si >= 0 and i + si < self.N and j + sj >= 0 and j + sj < self.N:
                        if self.cells_state[i + si][j + sj] == 0:
                            self.cells_state[i][j] = 0
                            self.cells_state[i + si][j + sj] = 1
                            move[i + si][j + sj] = 0
                            self.e[i + si][j + sj] = self.e[i][j]
                            self.life[i + si][j + sj] = self.life[i][j]
                            self.e[i][j] = 0
                            self.life[i][j] = 0

        # Размножение клеток
        done = [[1] * self.N for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j] == 1 and done[i][j] == 1:
                    if self.e[i][j] >= dr and self.life[i][j] >= T:
                        dest = 1
                        for k in range(i - 1, i + 2):
                            for l in range(j - 1, j + 2):
                                if (dest == 1 and l < self.N and l >= 0 and k < self.N and k >= 0 and (
                                        l != j or k != i)):
                                    self.cells_state[k][l] = 1
                                    self.e[i][j] -= dr
                                    self.e[k][l] = self.e[i][j]
                                    done[k][l] = 0
                                    self.life[k][l] = self.life[i][j]
                                    self.e[i][j] = 0
                                    self.life[i][j] = 0
                                    dest = 0

    def countAliveCells(self):
        alive = 0
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j] == 1:
                    alive += 1
        dead = self.N * self.N - alive
        return alive, dead

    def draw(self):
        self.screen.fill(self.WHITE)

        # Отрисовка клеток
        h = self.cell_size
        for i in range(self.N):
            for j in range(self.N):
                color = self.GREEN if self.cells_state[i][j] == 1 else self.WHITE
                pygame.draw.rect(self.screen, color, (j * h, i * h, h, h))
                # pygame.draw.rect(self.screen, self.BLACK, (j * h, i * h, h, h), 1)

        # Отображение информации
        alive, dead = self.countAliveCells()
        text = f"Такт: {self.count} | Живые: {alive} | Мёртвые: {dead}"
        text_surface = self.font.render(text, True, self.BLACK)
        self.screen.blit(text_surface, (20, 20))

        pygame.display.flip()

    def run(self):
        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    grid_x = x // self.cell_size
                    grid_y = y // self.cell_size
                    if 0 <= grid_x < self.N and 0 <= grid_y < self.N:
                        # Переключаем состояние клетки по клику мыши
                        self.cells_state[grid_y][grid_x] = 1 - self.cells_state[grid_y][grid_x]
                        if self.cells_state[grid_y][grid_x] == 1:
                            self.e[grid_y][grid_x] = p1 // 2  # Начальная энергия для клетки

            if not paused:
                self.action()
                self.count += 1
                print(f"Такт: {self.count}")

            self.draw()
            self.clock.tick(10)  # 10 FPS

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Размер N уменьшен для более наглядной визуализации
    # Вы можете установить исходное значение N=256, если нужно
    automaton = CellularAutomaton(900, 900, N=256)
    automaton.run()