import pygame
import sys
import numpy as np
import copy
import random
import matplotlib.pyplot as plt

WIDTH = 900
ROWS = 128

WIN = pygame.display.set_mode((WIDTH, WIDTH))

WHITE = (255, 255, 255)
BLACK = (255, 50, 255)


Pmax = 10
r = 1
A = 0.3
L = 15
T = 3
delta_p = 5
p1 = 35
delta_e = 2
delta_r = 3
N = 128


class Node:
    def __init__(self, row, col, width, energy, lifetime):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.energy = energy
        self.lifetime = lifetime
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour,
                         (self.x, self.y, WIDTH / 8, WIDTH / 8))


def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, 0, 0)
            grid[i].append(node)
    return grid


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def make_cells(rows, width):
    cells = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        cells.append([])
        for j in range(rows):
            cells[i].append(0)
    return cells


def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


def Find_Node(pos, WIDTH):
    interval = WIDTH / ROWS
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)


def neighbour(tile):
    col, row = tile.col, tile.row
    # print(row, col)
    neighbours = [[row - 1, col - 1], [row - 1, col], [row - 1, col + 1],
                  [row, col - 1], [row, col + 1],
                  [row + 1, col - 1], [row + 1, col], [row + 1, col + 1], ]
    actual = []
    for i in neighbours:
        row, col = i
        if 0 <= row <= (ROWS - 1) and 0 <= col <= (ROWS - 1):
            actual.append(i)
    # print(row, col, actual)
    return actual


def update_grid(oldgrid, time):
    newgrid = copy.deepcopy(oldgrid)

    fooding(plot, energy_individual)
    activity(energy_individual)
    death(individual_position, energy_individual, time_life)
    move(individual_position, energy_individual, time_life, plot)
    reproduction(individual_position, energy_individual, time_life)
    time(time_life)
    death(individual_position, energy_individual, time_life)

    return newgrid


def initial_data_individual_half(N):
    grid = []
    gap = WIDTH // ROWS
    print(gap)
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node = Node(i, j, gap, 0, 0)
            grid[i].append(node)

    k = 0
    while k < N*N*A:
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        # if y > int(N/2):
        if grid[x][y] != 1:
            grid[x][y].colour = BLACK
            grid[x][y].energy = 1
            grid[x][y].lifetime = 1
            k += 1

    return grid


def time(grid):

    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j].lifetime > 0:
                grid[i][j].lifetime += 1

    return grid


def plot_energy_update(plot):

    for i in range(len(plot)):
        for j in range(len(plot)):
            if plot[i][j] < Pmax:
                plot[i][j] += r

    return plot


def fooding(plot, grid):

    for i in range(len(plot)):
        for j in range(len(plot)):
            if grid[i][j].energy > 0:
                if plot[i][j] >= delta_p:
                    if grid[i][j].energy + delta_p <= p1:
                        grid[i][j].energy += delta_p
                        plot[i][j] -= delta_p
                    else:
                        grid[i][j].energy += p1
                        plot[i][j] -= p1 - grid[i][j].energy
                else:
                    grid[i][j].energy += plot[i][j]
                    plot[i][j] = 0

    return [plot, grid]


def activity(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid[i][j].energy -= delta_e

    return grid


def move(grid):

    check_move = np.zeros((len(grid), len(grid)))

    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 1 and check_move[i][j] == 0:
                x1 = i - 1
                x2 = i + 2
                y1 = j - 1
                y2 = j + 2
                if i == 0:
                    x1 = i
                if i == N - 1:
                    x2 = i + 1
                if j == 0:
                    y1 = j
                if j == N - 1:
                    y2 = j + 1

                summ = 0
                for k in range(x1, x2):
                    for m in range(y1, y2):
                        if grid[k][m].colour == BLACK:
                            summ += 1

                if summ < ((x2-x1) * (y2 - y1))-1:

                    k = i
                    l = j

                    while not (grid[k][l].colour == WHITE):
                        k = random.randint(x1, x2-1)
                        l = random.randint(y1, y2-1)

                    grid[k][l].colour = BLACK
                    grid[k][l].energy = grid[i][j].energy
                    grid[k][l].lifetime = grid[i][j].lifetime
                    check_move[k][l] = 1

                    grid[i][j].colour = WHITE
                    grid[i][j].energy = 0
                    grid[i][j].lifetime = 0
    return grid


def death(grid):
    N = len(grid)

    for i in range(N):
        for j in range(N):
            if (grid[i][j].lifetime > L or grid[i][j].energy <= 0):

                grid[i][j].lifetime = 0
                grid[i][j].colour = WHITE
                grid[i][j].energy = 0

    return grid


def reproduction(grid):

    N = len(grid)

    check_reproduction = np.zeros((N, N))

    for i in range(N):
        for j in range(N):
            if grid[i][j].colour == BLACK and grid[i][j].lifetime >= T and grid[i][j].energy > delta_r and check_reproduction[i][j] == 0:

                x1 = i - 1
                x2 = i + 2
                y1 = j - 1
                y2 = j + 2
                if i == 0:
                    x1 = i
                if i == N - 1:
                    x2 = i + 1
                if j == 0:
                    y1 = j
                if j == N - 1:
                    y2 = j + 1

                summ = 0
                for k in range(x1, x2):
                    for m in range(y1, y2):
                        if grid[k][m].colour == BLACK:
                            summ += 1
                
                if summ < ((x2-x1) * (y2 - y1))-1:

                    k = i
                    l = j

                    while not (grid[k][l].colour == WHITE):
                        k = random.randint(x1, x2-1)
                        l = random.randint(y1, y2-1)

                    grid[k][l].colour = BLACK
                    grid[k][l].energy = grid[i][j].energy - delta_r
                    grid[k][l].lifetime = grid[i][j].lifetime
                    check_reproduction[k][l] = 1
                    grid[k][l].lifetime = 1

                    grid[i][j].energy = delta_r
                    grid[i][j].lifetime = 1

    return grid


def max_array(arr):

    N = max(len(arr[0]), len(arr))
    M = min(len(arr[0]), len(arr))
    arr1 = np.copy(arr)
    max_arr = np.zeros((len(arr)*len(arr[0])))
    xy = np.zeros(((len(arr)*len(arr[0])), 2))
    for i in range(len(arr)*len(arr[0])):
        max_arr[i] = np.max(arr1)
        x = np.argmax(arr1)
        if N == len(arr[0]):
            xy[i] = [(int(x // N)), int(x % N)]
        else:
            xy[i] = [(int(x // M)), int(x % M)]
        arr1[int(xy[i][0])][int(xy[i][1])] = 0

    xy = np.array(xy, dtype=int)
    max_arr = np.array(max_arr, dtype=int)

    return [max_arr, xy]


def move(grid, plot):

    check_move = np.zeros((len(grid), len(grid)))

    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j].colour == BLACK and check_move[i][j] == 0:
                x1 = i - 1
                x2 = i + 2
                y1 = j - 1
                y2 = j + 2
                if i == 0:
                    x1 = i
                if i == N - 1:
                    x2 = i + 1
                if j == 0:
                    y1 = j
                if j == N - 1:
                    y2 = j + 1
                    
                summ = 0
                for k in range(x1, x2):
                    for m in range(y1, y2):
                        if grid[k][m].colour == BLACK:
                            summ += 1

                if summ < ((x2-x1) * (y2 - y1))-1 and np.max(plot[x1:x2, y1: y2]) != plot[i][j]:

                    max_neighborhood, xy_neighborhood = max_array(
                        plot[x1:x2, y1: y2])

                    for it in range((x2-x1) * (y2 - y1)-1):

                        k = xy_neighborhood[it][0]+x1
                        l = xy_neighborhood[it][1]+y1

                        if grid[k][l].colour == WHITE:

                            grid[k][l].colour = BLACK
                            grid[k][l].energy = grid[i][j].energy
                            grid[k][l].lifetime = grid[i][j].lifetime
                            check_move[k][l] = 1

                            grid[i][j].colour = WHITE
                            grid[i][j].energy = 0
                            grid[i][j].lifetime = 0

                            break
    return grid


def Modific(iter, N):

    plot = np.zeros((N, N)) + Pmax

    initial_all = initial_data_individual_half(N)
    individual_position = initial_all[0]
    energy_individual = initial_all[1]
    time_life = initial_all[2]

    print('Iter = {}'.format(0))

    for k in range(iter):

        fooding(plot, energy_individual)
        activity(energy_individual)
        death(individual_position, energy_individual, time_life)
        move(individual_position, energy_individual, time_life, plot)
        reproduction(individual_position, energy_individual, time_life)
        time(time_life)
        death(individual_position, energy_individual, time_life)
        plot_energy_update(plot)

        print('Iter = {}'.format(k + 1))
        if k > 14:
            pass
    plt.figure()
    return [plot, time_life, energy_individual]


run = True
grid = initial_data_individual_half(ROWS)
iter = 0

plot = np.zeros((N, N)) + Pmax



print('Iter = {}'.format(0))
update_display(WIN, grid, ROWS, WIDTH)

def count_alive(grid):
    count = 0
    for row in grid:
        for node in row:
            if node.colour == BLACK:
                count += 1
    return count
TAKT, ACTIVE = [], []

while run:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            run = False
    pygame.time.delay(50)

    fooding(plot, grid)
    activity(grid)
    death(grid)
    move(grid, plot)
    reproduction(grid)
    time(grid)
    death(grid)
    plot_energy_update(plot)

    update_display(WIN, grid, ROWS, WIDTH)
    #grid = update_grid(grid, time)
    # update_display(WIN, grid, ROWS, WIDTH)
    iter += 1
    active = count_alive(grid)
    print(iter, active )
    TAKT.append(iter)
    ACTIVE.append(active)
    # run= False
update_display(WIN, grid, ROWS, WIDTH)

import matplotlib.pyplot as plt
plt.plot(TAKT,ACTIVE)
plt.xlabel('Такт')
plt.ylabel('Кол-во живых клеток')
plt.show()