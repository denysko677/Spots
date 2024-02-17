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

# Функція для обробки подій
def handle_events(tiles):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
            x, y = pygame.mouse.get_pos()
            col = x // (SCREEN_WIDTH // GRID_SIZE)
            row = y // (SCREEN_HEIGHT // GRID_SIZE)
            index = row * GRID_SIZE + col
            if index >= 0 and index < GRID_SIZE ** 2:
                tile = tiles[index]
                empty_tile = [t for t in tiles if t.number == 0][0]
                if (tile.row == empty_tile.row and abs(tile.col - empty_tile.col) == 1) or \
                        (tile.col == empty_tile.col and abs(tile.row - empty_tile.row) == 1):
                    tile.row, empty_tile.row = empty_tile.row, tile.row
                    tile.col, empty_tile.col = empty_tile.col, tile.col
                    tiles[index], tiles[tiles.index(empty_tile)] = tiles[tiles.index(empty_tile)], tiles[index]

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

    clock = pygame.time.Clock()

    while True:
        handle_events(tiles)
        
        screen.fill(BLACK)

        for tile in tiles:
            tile.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
