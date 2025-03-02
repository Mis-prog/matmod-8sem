from gamelife import GameLife
import time
import os
import pygame
import sys

def main():
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
    screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
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

        # Ограничиваем FPS
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()