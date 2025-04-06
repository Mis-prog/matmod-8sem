import random
import math
from typing import List, Optional, Tuple

class CultureMediumAnimal:
    def __init__(self):
        self.IsAlive = True
        self.L = 15
        self.T = 0
        self.dE = 2
        self.dR = 3
        self.dP = 5
        self.Pmax = 35
        self.P = 5
    
    def ToAlive(self, current_cell):
        self.L -= 1
        self.T += 1
        if self.L < 1:
            self.IsAlive = False
        self.P -= self.dE
        if self.P < 1:
            self.IsAlive = False
        if not self.IsAlive:
            current_cell.Animal = None
    
    def ToEat(self, cell):
        if cell.P >= self.dP:
            if self.Pmax - self.P >= self.dP:
                cell.P -= self.dP
                self.P += self.dP
            else:
                cell.P -= self.Pmax - self.P
                self.P += self.Pmax - self.P
        else:
            if self.Pmax - self.P >= cell.P:
                self.P += cell.P
                cell.P = 0
            else:
                self.P += self.Pmax - self.P
                cell.P -= self.Pmax - self.P
    
    def ToJump(self, current_cell, new_cell):
        new_cell.Animal = current_cell.Animal
        new_cell.AnimalAte = True
        current_cell.Animal = None
        young, is_correct = new_cell.Animal.GiveBirth()
        if is_correct:
            current_cell.Animal = young
    
    def GiveBirth(self):
        new_animal = CultureMediumAnimal()
        is_correct = False
        if self.T >= 3 and self.P > self.dR:
            self.P -= self.dR
            is_correct = True
        return new_animal, is_correct


class CultureMediumCell:
    def __init__(self):
        self.Pmax = 10
        self.P = 10
        self.dP = 1
        self.Animal = None
        self.AnimalAte = False
    
    def NewEra(self):
        self.AnimalAte = False
        if self.P < self.Pmax:
            self.P += self.dP

class CultureMedium1:
    def __init__(self, distribution_ratio, size):
        self.Rand = random.Random()
        self.Size = size
        self.DistributionRatio = distribution_ratio
        self.Generation = self.GetZeroGeneration(distribution_ratio, size)
    
    def GetZeroGeneration(self, distribution_ratio, size):
        result = [[CultureMediumCell() for _ in range(size)] for _ in range(size)]
        
        amount_cell = int(round(size * size * distribution_ratio))
        cells_list = []
        
        for i in range(amount_cell):
            value = self.Rand.randint(0, size * size - 1)
            cells_list.append(value)
            row = value // size
            col = value % size
            result[row][col].Animal = CultureMediumAnimal()
        
        return result
    
    def UpdateGeneration(self):
        for i in range(self.Size):
            for j in range(self.Size):
                self.Generation[i][j].NewEra()
        
        # Обрабатываем углы
        self.JumpCell(self.Generation[0][0],
                     [self.Generation[0][1],
                      self.Generation[1][0],
                      self.Generation[1][1]])
        
        self.JumpCell(self.Generation[self.Size-1][0],
                     [self.Generation[self.Size-1][1],
                      self.Generation[self.Size-2][0],
                      self.Generation[self.Size-2][1]])
        
        self.JumpCell(self.Generation[0][self.Size-1],
                     [self.Generation[0][self.Size-2],
                      self.Generation[1][self.Size-2],
                      self.Generation[1][self.Size-1]])
        
        self.JumpCell(self.Generation[self.Size-1][self.Size-1],
                     [self.Generation[self.Size-2][self.Size-2],
                      self.Generation[self.Size-1][self.Size-2],
                      self.Generation[self.Size-2][self.Size-1]])
        
        # Обрабатываем края
        for i in range(1, self.Size - 1):
            self.JumpCell(self.Generation[0][i],
                         [self.Generation[0][i-1],
                          self.Generation[0][i+1],
                          self.Generation[1][i-1],
                          self.Generation[1][i],
                          self.Generation[1][i+1]])
            
            self.JumpCell(self.Generation[self.Size-1][i],
                         [self.Generation[self.Size-1][i-1],
                          self.Generation[self.Size-1][i+1],
                          self.Generation[self.Size-2][i],
                          self.Generation[self.Size-2][i-1],
                          self.Generation[self.Size-2][i+1]])
            
            self.JumpCell(self.Generation[i][0],
                         [self.Generation[i-1][0],
                          self.Generation[i+1][0],
                          self.Generation[i][1],
                          self.Generation[i-1][1],
                          self.Generation[i+1][1]])
            
            self.JumpCell(self.Generation[i][self.Size-1],
                         [self.Generation[i-1][self.Size-1],
                          self.Generation[i+1][self.Size-1],
                          self.Generation[i][self.Size-2],
                          self.Generation[i-1][self.Size-2],
                          self.Generation[i+1][self.Size-2]])
        
        # Обрабатываем внутреннюю часть
        for i in range(1, self.Size - 1):
            for j in range(1, self.Size - 1):
                self.JumpCell(self.Generation[i][j],
                             [self.Generation[i-1][j],
                              self.Generation[i+1][j],
                              self.Generation[i][j-1],
                              self.Generation[i-1][j-1],
                              self.Generation[i+1][j-1],
                              self.Generation[i][j+1],
                              self.Generation[i-1][j+1],
                              self.Generation[i+1][j+1]])
    
    def JumpCell(self, current_cell, cells):
        if current_cell.Animal is not None:
            current_cell.Animal.ToAlive(current_cell)
            if current_cell.Animal is not None:
                current_cell.Animal.ToEat(current_cell)
                
                empty_cells = [cell for cell in cells if cell.Animal is None]
                if len(empty_cells) > 0:
                    index = self.Rand.randint(0, len(empty_cells) - 1) if len(empty_cells) > 1 else 0
                    current_cell.Animal.ToJump(current_cell, empty_cells[index])
    
    def CurrentGenerationToString(self):
        active_cells = 0
        passive_cells = 0
        dead_cells = 0
        
        result = []
        
        for i in range(self.Size):
            row = []
            for j in range(self.Size):
                if self.Generation[i][j].Animal is not None:
                    row.append('O')
                    active_cells += 1
                else:
                    row.append(' ')
                    dead_cells += 1
            result.append(''.join(row))
        
        return '\n'.join(result), active_cells, passive_cells, dead_cells
    
    
class CultureMedium2:
    def __init__(self, distribution_ratio: float, size: int):
        self.Size = size
        self.distribution_ratio = distribution_ratio
        self.rand = random.Random()
        self.generation = self._get_zero_generation(distribution_ratio, size)
        # self.generation = self._get_cycle_generation(distribution_ratio, size)

    def _get_zero_generation(self, distribution_ratio: float, size: int):
        generation = [[CultureMediumCell() for _ in range(size)] for _ in range(size)]

        amount_cell = round(size * size * distribution_ratio)
        used = set()

        while len(used) < amount_cell:
            value = self.rand.randint(0, size * size - 1)
            if value not in used:
                used.add(value)
                i, j = divmod(value, size)
                generation[i][j].animal = CultureMediumAnimal()

        return generation

    def update_generation(self):
        for row in self.generation:
            for cell in row:
                cell.new_era()

        g = self.generation
        s = self.size

        self._jump_cell(g[0][0], g[0][1], g[1][0], g[1][1])
        self._jump_cell(g[s - 1][0], g[s - 1][1], g[s - 2][0], g[s - 2][1])
        self._jump_cell(g[0][s - 1], g[0][s - 2], g[1][s - 2], g[1][s - 1])
        self._jump_cell(g[s - 1][s - 1], g[s - 2][s - 2], g[s - 1][s - 2], g[s - 2][s - 1])

        for i in range(1, s - 1):
            self._jump_cell(g[0][i], g[0][i - 1], g[0][i + 1], g[1][i - 1], g[1][i], g[1][i + 1])
            self._jump_cell(g[s - 1][i], g[s - 1][i - 1], g[s - 1][i + 1], g[s - 2][i], g[s - 2][i - 1], g[s - 2][i + 1])
            self._jump_cell(g[i][0], g[i - 1][0], g[i + 1][0], g[i][1], g[i - 1][1], g[i + 1][1])
            self._jump_cell(g[i][s - 1], g[i - 1][s - 1], g[i + 1][s - 1], g[i][s - 2], g[i - 1][s - 2], g[i + 1][s - 2])

        for i in range(1, s - 1):
            for j in range(1, s - 1):
                self._jump_cell(
                    g[i][j],
                    g[i - 1][j], g[i + 1][j], g[i][j - 1], g[i - 1][j - 1],
                    g[i + 1][j - 1], g[i][j + 1], g[i - 1][j + 1], g[i + 1][j + 1]
                )

    def _jump_cell(self, current_cell: CultureMediumCell, *cells: CultureMediumCell):
        if current_cell.animal:
            current_cell.animal.to_alive(current_cell)
            if current_cell.animal:
                current_cell.animal.to_eat(current_cell)
                empty_cells = [c for c in cells if c.animal is None]
                if empty_cells:
                    max_cell = max(empty_cells, key=lambda c: c.p)
                    if max_cell.p > current_cell.p:
                        current_cell.animal.to_jump(current_cell, max_cell)

    def current_generation_to_string(self) -> Tuple[str, int, int, int]:
        active_cells = 0
        passive_cells = 0  # не используется в C# коде
        dead_cells = 0

        result = []
        for row in self.generation:
            line = ""
            for cell in row:
                if cell.animal:
                    line += "O"
                    active_cells += 1
                else:
                    line += " "
                    dead_cells += 1
            result.append(line)

        return "\n".join(result), active_cells, passive_cells, dead_cells

# Импортируем необходимые модули
import time

# Создаем среду с соотношением распределения 0.3 и размером 20x20
culture = CultureMedium2(distribution_ratio=0.3, size=20)


# ACTIVE, DEAD = [],[]
# # Запускаем симуляцию на 50 поколений
# for generation in range(100):
#     # Выводим текущее состояние
#     gen_str, active, passive, dead = culture.CurrentGenerationToString()
#     print(f"Поколение {generation}:")
#     print(gen_str)
#     print(f"Активных клеток: {active}, Мертвых клеток: {dead}")
#     ACTIVE.append(active)
#     DEAD.append(dead)
    
    
#     # Обновляем поколение
#     culture.UpdateGeneration()
    
#     # Пауза для визуализации (если нужно)
#     time.sleep(0.1)

import pygame 
    
class CultureVisualizer:
    def __init__(self, culture_medium, cell_size=20, fps=10):
        self.culture = culture_medium
        self.cell_size = cell_size
        self.fps = fps
        self.width = culture_medium.Size * cell_size
        self.height = culture_medium.Size * cell_size
        
        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Culture Medium Simulation")
        self.clock = pygame.time.Clock()
        
        # Цвета
        self.BACKGROUND = (240, 240, 240)  # Светло-серый фон
        self.GRID_COLOR = (200, 200, 200)  # Цвет сетки
        self.ANIMAL_COLOR = (0, 100, 255)  # Цвет животных
        self.RESOURCE_COLOR = (0, 180, 0)  # Цвет для отображения ресурсов
        
        self.font = pygame.font.SysFont(None, 24)
        self.generation = 0
        self.running = True
    
    def draw_grid(self):
        """Отрисовка сетки"""
        for i in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.GRID_COLOR, (i, 0), (i, self.height))
        for j in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.GRID_COLOR, (0, j), (self.width, j))
    
    def draw_cells(self):
        """Отрисовка клеток и животных"""
        for i in range(self.culture.Size):
            for j in range(self.culture.Size):
                cell = self.culture.Generation[i][j]
                x = j * self.cell_size
                y = i * self.cell_size
                
                # Отрисовка уровня ресурсов клетки
                # resource_height = int((cell.P / cell.Pmax) * self.cell_size)
                # resource_rect = pygame.Rect(
                #     x, 
                #     y + self.cell_size - resource_height, 
                #     self.cell_size, 
                #     resource_height
                # )
                # resource_color = (0, int(150 * (cell.P / cell.Pmax)) + 50, 0)
                # pygame.draw.rect(self.screen, resource_color, resource_rect)
                
                # Отрисовка животного, если он есть
                if cell.Animal is not None:
                    # Рисуем круг, цвет зависит от энергии и возраста
                    energy_ratio = cell.Animal.P / cell.Animal.Pmax
                    age_ratio = cell.Animal.T / cell.Animal.L
                    
                    # Цвет зависит от энергии (от синего к красному)
                    # animal_color = (
                    #     int(255 * (1 - energy_ratio)),  # R
                    #     50,                             # G
                    #     int(255 * energy_ratio)         # B
                    # )
                    
                    animal_color = (
                        255,  # R
                        50,                             # G
                        255         # B
                    )
                    
                    # Размер зависит от возраста
                    # radius = int(self.cell_size * 0.4 * (1 - age_ratio * 0.5))
                    radius = 2
                    
                    pygame.draw.circle(
                        self.screen, 
                        animal_color, 
                        (x + self.cell_size // 2, y + self.cell_size // 2), 
                        radius
                    )
    
    def draw_stats(self):
        """Отрисовка статистики"""
        _, active, _, dead = self.culture.CurrentGenerationToString()
        total = active + dead
        active_percent = (active / total * 100) if total > 0 else 0
        
        stats_text = f"Gen: {self.generation} | Animals: {active} ({active_percent:.1f}%)"
        text_surface = self.font.render(stats_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))
    
    def handle_events(self):
        """Обработка событий Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Пауза/возобновление (можно добавить)
                    pass
    
    def run(self, max_generations=None):
        """Основной цикл симуляции"""
        TAKT, ACTIVE = [], []
        i = 0 
        while self.running:
            # Обработка событий
            self.handle_events()
            
            # Отрисовка
            self.screen.fill(self.BACKGROUND)
            self.draw_grid()
            self.draw_cells()
            self.draw_stats()
            pygame.display.flip()
            
            # Обновление состояния
            
            gen_str, active, passive, dead = self.culture.CurrentGenerationToString()
            i+=1   
            TAKT.append(i)
            ACTIVE.append(active)

            self.culture.UpdateGeneration()
            
            self.generation += 1
            
            # Проверка условия остановки
            if max_generations is not None and self.generation >= max_generations:
                self.running = False
            
            # Контроль FPS
            self.clock.tick(self.fps)
        
        pygame.quit()
        
        return TAKT, ACTIVE

if __name__ == "__main__":
    # Параметры симуляции
    SIZE = 256 # Размер сетки
    DISTRIBUTION = 0.3  # Начальная плотность животных
    
    # Создаем среду
    culture = CultureMedium2(distribution_ratio=DISTRIBUTION, size=SIZE)
    
    # Создаем и запускаем визуализатор
    visualizer = CultureVisualizer(culture, cell_size=5, fps=30)
    
    TAKT, ACTIVE = visualizer.run()
    
    import matplotlib.pyplot as plt 
    
    
    plt.plot(TAKT,ACTIVE)
    plt.xlabel('Такт')
    plt.ylabel('Кол-во живых особей')
    plt.show()