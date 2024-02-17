# game.py

import pygame
import sys
import random

# Задаємо розмір сітки для гри
GRID_SIZE = 4

# Задаємо розміри екрану
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# Задаємо кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Клас, що представляє кожну плитку у грі
class Tile:
    def __init__(self, number, row, col):
        self.number = number
        self.row = row
        self.col = col
        self.width = SCREEN_WIDTH // GRID_SIZE
        self.height = SCREEN_HEIGHT // GRID_SIZE
        self.rect = pygame.Rect(col * self.width, row * self.height, self.width, self.height)

    def draw(self, screen):
        if self.number == 0:
            pygame.draw.rect(screen, GRAY, self.rect)
        else:
            pygame.draw.rect(screen, WHITE, self.rect)
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.number), True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

# Функція для створення нової гри
def new_game():
    numbers = list(range(GRID_SIZE ** 2))
    random.shuffle(numbers)
    grid = [[numbers.pop() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid

# Головна функція гри
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("П'ятнашки")

    grid = new_game()

    tiles = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tiles.append(Tile(grid[row][col], row, col))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        for tile in tiles:
            tile.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
