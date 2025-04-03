import pygame
import sys
import numpy as np
import copy
WIDTH = 900
ROWS = 128

WIN = pygame.display.set_mode((WIDTH, WIDTH))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (107, 142, 35)
A = 0.7
P = 3
T = 5
B = 8

class Node:
    def __init__(self, row, col, width, tick, level, livetime):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.tick = tick
        self.actLevel = level
        self.livetime = livetime
        self.colour = WHITE
        self.occupied = None
        
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))
        
def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, 0, 0, 0)
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
        if 0 <= col <= (ROWS - 1):
            if row < 0:
                row = -1
            if row == ROWS:
                row = 0
            actual.append([row, col])
    return actual

def update_grid(oldgrid, time):
    newgrid = copy.deepcopy(oldgrid)
   
    for row in newgrid:
        for tile in row:

            if oldgrid[tile.row][tile.col].colour == WHITE:
                tile.actLevel *= A
                neighbours = neighbour(oldgrid[tile.row][tile.col])
                summ = oldgrid[tile.row][tile.col].actLevel
                for i in neighbours:
                    row2, col2 = i
                    summ += oldgrid[row2][col2].actLevel
                
                if summ >= P:
                    tile.colour = YELLOW
                    tile.tick = time + T
                    tile.actLevel = 1
            
            if oldgrid[tile.row][tile.col].colour == BLACK:
                tile.actLevel *= A
                
                if oldgrid[tile.row][tile.col].tick == time:
                    tile.colour = WHITE
                    tile.tick = 0
                    
            if oldgrid[tile.row][tile.col].colour == YELLOW:
                if oldgrid[tile.row][tile.col].tick == time:
                    tile.colour = BLACK
                    tile.tick = time + B
                    tile.actLevel *= A
                else:
                    tile.actLevel = 1
                    tile.colour = YELLOW

            #oldgrid[tile.row][tile.col].livetime -= 1
            # newgrid[tile.row][tile.col].livetime -= 1
            # if oldgrid[tile.row][tile.col].colour == WHITE:
            #     tile.actLevel *= A
            #     neighbours = neighbour(oldgrid[tile.row][tile.col])
            #     summ = oldgrid[tile.row][tile.col].actLevel
            #     for i in neighbours:
            #         row2, col2 = i
            #         summ += oldgrid[row2][col2].actLevel
                
            #     if summ >= P:
            #         tile.colour = YELLOW
            #         tile.livetime = T
            #         tile.actLevel = 1
            
            # if oldgrid[tile.row][tile.col].colour == BLACK:
            #     tile.actLevel *= A
                
            #     if oldgrid[tile.row][tile.col].livetime == 0:
            #         tile.colour = WHITE
            #         tile.livetime = 0
                    
                    
            # if oldgrid[tile.row][tile.col].colour == YELLOW:
            #     if oldgrid[tile.row][tile.col].livetime == 0:
            #         tile.colour = BLACK
            #         tile.tick = time + B
            #         tile.actLevel *= A
            #     else:
            #         tile.actLevel = 1
            #         tile.colour = YELLOW
            #         tile.livetime -= 1
            
    return newgrid


run = True
grid = make_grid(ROWS, WIDTH)
time = 0

# for i in range(len(grid) - 7, len(grid) - 5):
#     for j in range(20,len(grid[0])-20):
#         grid[i][j].colour = YELLOW
#         grid[i][j].actLevel = 1
#         grid[i][j].livetime = T
#         grid[i][j].tick = T

for i in range(len(grid)):
    for j in range(len(grid[0]) - 7,len(grid[0]) - 6):
        grid[i][j].colour = YELLOW
        grid[i][j].actLevel = 1
        grid[i][j].livetime = T
        grid[i][j].tick = T


for i in range(len(grid)):
    for j in range(2,3):
        grid[i][j].colour = YELLOW
        grid[i][j].actLevel = 1
        grid[i][j].livetime = T
        grid[i][j].tick = T
    

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            run = False
    pygame.time.delay(50)
    
    
    if time % 15 == 0:
        for i in range(int(len(grid) / 2 - 1), int(len(grid) / 2 + 2)):
            for j in range(int(len(grid[0]) / 2 - 1), int(len(grid[0]) / 2 + 2)):
                grid[i][j].colour = YELLOW
                grid[i][j].actLevel = 1
                grid[i][j].livetime = T
                grid[i][j].tick = time + T
    
    grid = update_grid(grid, time)  
    update_display(WIN, grid, ROWS, WIDTH)
    print(time)
    time += 1
    #run= False
update_display(WIN, grid, ROWS, WIDTH)