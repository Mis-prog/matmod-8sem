import pygame
import sys
import random
import numpy as np
import matplotlib

matplotlib.use('Agg')  # Важно для интеграции с pygame
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
from io import BytesIO

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

ACTIVE, COUNT = [], []


class CellularAutomaton:
    def __init__(self, width, height, N=100):
        pygame.init()
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((width, height))  # Добавляем 400 пикселей для графика
        pygame.display.set_caption("Pygame Cellular Automaton with Graph")
        self.clock = pygame.time.Clock()

        self.N = N
        self.cell_size = min(width, height) // N
        # self.cell_size = 3.3
        # Инициализация состояний клеток
        self.cells_state = [[0] * self.N for i in range(self.N)]
        self.p = [[pmax] * self.N for i in range(self.N)]
        self.e = [[0] * self.N for i in range(self.N)]
        self.life = [[0] * self.N for i in range(self.N)]
        self.count = 0

        # Инициализация случайных живых клеток
        for i in range(int(A * N * N)):
            self.cells_state[random.randint(0, int((self.N - 1)*0.6))][random.randint(0, int((self.N - 1) * 1))] = 1
        # for i in range(int(N)):
        #     self.cells_state[i][int((self.N - 1)*0.5)] = 1

        # Цвета
        self.WHITE = (255, 255, 255)
        self.GREEN = (139, 0, 255)
        self.BLACK = (240, 240, 240)
        self.GRAY = (169, 169, 169)

        # Шрифт для отображения информации
        self.font = pygame.font.SysFont('Arial', 20, True)

        # Данные для графика
        self.count_history = []
        self.alive_history = []
        self.energy_history = []
        self.zrelye_history = []
        self.newborn_history = []
        self.death_history = []
        self.age_histories = []
        self.death_by_age_total = [0] * (L + 1)  # итоговая статистика по возрастам
        self.death_by_age = [0] * (L + 1)  # на текущем такте
        print("cdfdsf",len(self.death_by_age))
        self.death_age_histories = []  # история по тактам

        # Создаем объект Figure для графика
        self.fig, self.ax = plt.subplots(1, 1, figsize=(6, 6), dpi=80)
        self.fig.patch.set_facecolor((0.9, 0.9, 0.9))
        self.canvas = agg.FigureCanvasAgg(self.fig)

    def action(self):
        death_count = 0

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
                        dead_age = self.life[i][j]
                        # print(dead_age)
                        if dead_age >= len(self.death_by_age):
                            dead_age = len(self.death_by_age) - 1
                        self.death_by_age[dead_age] += 1
                        self.life[i][j] = 0
                        death_count += 1

        # Движение клеток
        move = [[1] * self.N for i in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j] == 1 and move[i][j] == 1:
                    neighbors = [(di, dj) for di in range(-1, 2) for dj in range(-1, 2) if not (di == 0 and dj == 0)]
                    random.shuffle(neighbors)
                    bk = i
                    bl = j
                    bp = self.p[i][j]

                    for di, dj in neighbors:
                        k = i + di
                        l = j + dj
                        if 0 <= k < self.N and 0 <= l < self.N:
                            if self.cells_state[k][l] == 0:
                                if self.p[k][l] > bp:
                                    bk = k
                                    bl = l
                                    bp = self.p[k][l]

                    # Обновление состояния клеток
                    move[bk][bl] = 0
                    if bk != i or bl != j:
                        self.cells_state[i][j] = 0
                        self.cells_state[bk][bl] = 1
                        self.e[bk][bl] = self.e[i][j]
                        self.life[bk][bl] = self.life[i][j]
                        self.e[i][j] = 0
                        self.life[i][j] = 0

        newborn_count = 0
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
                                    newborn_count += 1
                                    self.e[i][j] -= dr
                                    self.e[k][l] = self.e[i][j]
                                    done[k][l] = 0
                                    self.life[k][l] = self.life[i][j]
                                    self.e[i][j] = 0
                                    self.life[i][j] = 0
                                    dest = 0

        # Обновление данных для графика
        # alive, _ = self.countAliveCells()

        from collections import defaultdict

        alive = 0
        zrelye = 0
        total_energy = 0
        age_hist = [0] * (L + 1)
        for i in range(self.N):
            for j in range(self.N):
                if self.cells_state[i][j] == 1:
                    age = self.life[i][j]
                    if age <= L:
                        age_hist[age] += 1
                    alive += 1
                    total_energy += self.e[i][j]
                    if self.life[i][j] >= T:
                        zrelye += 1
        self.death_age_histories.append(self.death_by_age[:])
        for i in range(L + 1):
            self.death_by_age_total[i] += self.death_by_age[i]
        self.death_by_age = [0] * (L + 1)

        self.alive_history.append(alive)
        self.energy_history.append(total_energy)
        self.zrelye_history.append(zrelye)
        self.count_history.append(self.count)
        self.newborn_history.append(newborn_count)
        self.death_history.append(death_count)
        self.age_histories.append(age_hist)

        max_life = max(max(row) for row in self.life)
        print(f'Максимальная продолжительность жизни клеток: {max_life}')

        # # Ограничиваем историю для экономии памяти
        # if len(self.count_history) > 100:
        #     self.count_history.pop(0)
        #     self.alive_history.pop(0)

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

        max_j = self.width // self.cell_size
        # Отрисовка клеток
        for i in range(int(self.N)):
            for j in range(int(self.N)):
                color = self.GREEN if self.cells_state[i][j] == 1 else self.WHITE
                pygame.draw.rect(self.screen, color, (j * self.cell_size, i * self.cell_size,
                                                      self.cell_size, self.cell_size))
                # pygame.draw.rect(self.screen, self.BLACK, (j * self.cell_size, i * self.cell_size,
                #                                            self.cell_size, self.cell_size), 1)

        # Отображение графика справа
        # graph_surf = self.update_graph()
        # self.screen.blit(graph_surf, (self.width, 50))
        # self.draw_grid()

        # Отображение информации
        alive, dead = self.countAliveCells()
        text = f"Такт: {self.count} | Живые: {alive} | Мёртвые: {dead}"
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (0, 100))

        # Добавляем инструкции
        instructions = [
            "Управление:",
            "Пробел - пауза/продолжить",
            "Клик мышью - добавить/удалить клетку"
        ]

        y_offset = self.height - 80
        for instruction in instructions:
            instr_surf = self.font.render(instruction, True, self.BLACK)
            self.screen.blit(instr_surf, (self.width + 10, y_offset))
            y_offset += 20

        pygame.display.flip()

    def run(self):
        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        plt.plot(self.count_history, self.alive_history, label='Кол-во живых')
                        plt.plot(self.count_history, self.zrelye_history, label='Кол-во зрелых')
                        plt.plot(self.count_history, self.energy_history, label='Кол-во энергии')
                        plt.xlabel('Такт')
                        plt.legend()
                        plt.savefig("active_cells_plot.png")
                        np.savez("metrics.npz",
                                 count=self.count_history,
                                 energy=self.energy_history,
                                 zrelye=self.zrelye_history,
                                 alive=self.alive_history,
                                 death=self.death_history,
                                 newborn=self.newborn_history)
                        age_history = np.array(self.age_histories)
                        death_age_histories = np.array(self.death_age_histories)
                        np.save("age_history.npy", age_history)
                        np.save("death_age_histories.npy", death_age_histories)

                        running = False

                    # elif event.type == pygame.MOUSEBUTTONDOWN:
                    # x, y = pygame.mouse.get_pos()
                    # if x < self.width:  # Только в пределах сетки
                    #     grid_x = x // self.cell_size
                    #     grid_y = y // self.cell_size
                    #     if 0 <= grid_x < self.N and 0 <= grid_y < self.N:
                    #         # Переключаем состояние клетки по клику мыши
                    #         self.cells_state[grid_y][grid_x] = 1 - self.cells_state[grid_y][grid_x]
                    #         if self.cells_state[grid_y][grid_x] == 1:
                    #             self.e[grid_y][grid_x] = p1 // 2  # Начальная энергия для созданной клетки

            if not paused:
                self.action()
                self.count += 1
                print(f"Такт: {self.count}")

            self.draw()
            self.clock.tick(5)  # 10 FPS

        pygame.quit()
        plt.close(self.fig)  # Закрываем фигуру matplotlib
        sys.exit()

    def draw_grid(self):
        """Функция для отрисовки сетки."""
        for i in range(1, self.N):
            # Вертикальные линии
            pygame.draw.line(self.screen, self.GRAY, (i * self.cell_size, 0), (i * self.cell_size, self.height), 1)
            # Горизонтальные линии
            pygame.draw.line(self.screen, self.GRAY, (0, i * self.cell_size), (self.width, i * self.cell_size), 1)


if __name__ == "__main__":
    # Создаем экземпляр автомата с размерами основной сетки 800x800
    # и графиком справа шириной 400 пикселей
    automaton = CellularAutomaton(1000, 1000, N=256)
    automaton.run()

    plt.plot(COUNT, ACTIVE)
    plt.show()
