import pygame
import sys
import numpy as np
from random import choice
WIDTH = 900
ROWS = 50
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Game of Life")
WHITE = (255, 255, 255)
BLACK = (107, 142, 35)
class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = choice([WHITE, BLACK])
        # self.colour = WHITE
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
            node = Node(j, i, gap)
            grid[i].append(node)
    return grid

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
"""
The nodes are all white so this we need to draw the grey lines that separate all the chess tiles
from each other and that is what this function does"""
def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()
def Find_Node(pos, WIDTH):
    interval = WIDTH / ROWS
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)
def neighbour(tile):
    col, row = tile.row, tile.col
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
def update_grid(grid):
    newgrid = []
    for row in grid:
        for tile in row:
            neighbours = neighbour(tile)
            count = 0
            for i in neighbours:
                row, col = i
                if grid[row][col].colour == BLACK:
                    count += 1
            if tile.colour == BLACK:
                if count == 2 or count == 3:
                    newgrid.append(BLACK)
                else:
                    newgrid.append(WHITE)
            else:
                if count == 3:
                    newgrid.append(BLACK)
                else:
                    newgrid.append(WHITE)
    return newgrid

def main(WIN, WIDTH):
    run = None
    grid = make_grid(ROWS, WIDTH)
    while True:
        pygame.time.delay(50)  ##stops cpu dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = True
                    cells_str = '\n'.join([''.join([str(int(tile.colour==BLACK)) 
                                                for tile in row ]) for row in grid])
                    f = open( '1st.txt', 'w' )
                    f.write( cells_str )
                    f.close()
                    print(cells_str)
                    print('\n')
                if event.key == pygame.K_o:
                    cells = cells_str.split('\n')
                    print('-----------------------------------------------------')
                    print(cells)
                    print('-----------------------------------------------------')
                    for i in range(len(cells)):
                        for j in range(len(cells[i])):
                            grid[i][j].colour = BLACK if cells[i][j] == '1' else WHITE
                if event.key == pygame.K_l:
                    f = open('1st.txt', 'r')
                    cells = []
                    #with open('1st.txt') as f:
                    #   cells = f.readlines()
                    
                    #cells = [i.strip() for i in cells]
                    #for eachLine in f:
                        #cells.append(eachLine.strip('\n').split(' '))
                    #f.close()
                    content = f.read()
                    cells = content.splitlines()
                    f.close()
                    print(cells)
                    for i in range(len(cells)):
                        for j in range(len(cells[i])):
                            grid[i][j].colour = BLACK if cells[i][j] == '1' else WHITE
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = Find_Node(pos, WIDTH)
                if grid[col][row].colour == WHITE:
                    grid[col][row].colour = BLACK
                elif grid[col][row].colour == BLACK:
                    grid[col][row].colour = WHITE
            
            while run:
                
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        run = False
                pygame.time.delay(50)
                newcolours = update_grid(grid)
                
                count=0
                for i in range(0,len(grid[0])):
                    for j in range(0, len(grid[0])):
                        grid[i][j].colour=newcolours[count]
                        
                    
                        count+=1
                    
                update_display(WIN, grid, ROWS, WIDTH)
                #run= False
            update_display(WIN, grid, ROWS, WIDTH)
main(WIN, WIDTH)