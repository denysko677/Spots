import pygame
import sys
import random

# Глобальні змінні
GRID_SIZE = 4
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

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

def new_game():
    numbers = list(range(GRID_SIZE ** 2))
    random.shuffle(numbers)
    grid = [[numbers.pop() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid

def get_clicked_tile_index(tiles, x, y):
    col = x // (SCREEN_WIDTH // GRID_SIZE)
    row = y // (SCREEN_HEIGHT // GRID_SIZE)
    index = row * GRID_SIZE + col
    return index if 0 <= index < len(tiles) else None

def get_valid_neighbors(index):
    neighbors = []
    row, col = index // GRID_SIZE, index % GRID_SIZE
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
            neighbors.append(new_row * GRID_SIZE + new_col)
    return neighbors

def shuffle_tiles(tiles, empty_tile_index, steps=100):
    for _ in range(steps):
        valid_neighbors = get_valid_neighbors(empty_tile_index)
        random_neighbor_index = random.choice(valid_neighbors)
        tiles[empty_tile_index], tiles[random_neighbor_index] = tiles[random_neighbor_index], tiles[empty_tile_index]
        empty_tile_index = random_neighbor_index

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("П'ятнашки")

    grid = new_game()

    tiles = [Tile(grid[row][col], row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE)]

    empty_tile_index = GRID_SIZE ** 2 - 1

    shuffle_tiles(tiles, empty_tile_index)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                clicked_tile_index = get_clicked_tile_index(tiles, x, y)
                if clicked_tile_index is not None:
                    if clicked_tile_index in get_valid_neighbors(empty_tile_index):
                        tiles[empty_tile_index], tiles[clicked_tile_index] = tiles[clicked_tile_index], tiles[empty_tile_index]
                        empty_tile_index = clicked_tile_index

        screen.fill(BLACK)
        for tile in tiles:
            tile.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
