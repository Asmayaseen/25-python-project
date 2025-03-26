import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GAME_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GAME_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (128, 0, 128),  # Purple
]

# Tetromino Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I Shape
    [[1, 1], [1, 1]],  # O Shape
    [[0, 1, 0], [1, 1, 1]],  # T Shape
    [[1, 0, 0], [1, 1, 1]],  # L Shape
    [[0, 0, 1], [1, 1, 1]],  # J Shape
    [[1, 1, 0], [0, 1, 1]],  # S Shape
    [[0, 1, 1], [1, 1, 0]],  # Z Shape
]

# Game Grid
def create_grid():
    return [[BLACK for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]

# Draw Grid
def draw_grid(screen, grid):
    for y in range(GAME_HEIGHT):
        for x in range(GAME_WIDTH):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for x in range(GAME_WIDTH):
        pygame.draw.line(screen, GREY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    for y in range(GAME_HEIGHT):
        pygame.draw.line(screen, GREY, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))

# Tetromino Class
class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GAME_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Check Collision
def check_collision(tetromino, grid, dx=0, dy=0):
    for y, row in enumerate(tetromino.shape):
        for x, value in enumerate(row):
            if value:
                new_x = tetromino.x + x + dx
                new_y = tetromino.y + y + dy
                if new_x < 0 or new_x >= GAME_WIDTH or new_y >= GAME_HEIGHT or grid[new_y][new_x] != BLACK:
                    return True
    return False

# Merge Tetromino to Grid
def merge_tetromino(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, value in enumerate(row):
            if value:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

# Clear Rows
def clear_rows(grid):
    full_rows = [row for row in grid if all(color != BLACK for color in row)]
    for _ in full_rows:
        grid.pop(grid.index(_))
        grid.insert(0, [BLACK for _ in range(GAME_WIDTH)])
    return len(full_rows)

# Main Game
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    grid = create_grid()
    current_piece = Tetromino()
    next_piece = Tetromino()
    score = 0
    fall_time = 0
    game_over = False

    while not game_over:
        screen.fill(BLACK)
        fall_speed = 0.3
        fall_time += clock.get_rawtime()
        clock.tick()

        # Piece Falling
        if fall_time / 1000 >= fall_speed:
            if not check_collision(current_piece, grid, dy=1):
                current_piece.y += 1
            else:
                merge_tetromino(current_piece, grid)
                score += clear_rows(grid)
                current_piece = next_piece
                next_piece = Tetromino()
                if check_collision(current_piece, grid):
                    game_over = True
            fall_time = 0

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(current_piece, grid, dx=-1):
                    current_piece.x -= 1
                elif event.key == pygame.K_RIGHT and not check_collision(current_piece, grid, dx=1):
                    current_piece.x += 1
                elif event.key == pygame.K_DOWN and not check_collision(current_piece, grid, dy=1):
                    current_piece.y += 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if check_collision(current_piece, grid):
                        for _ in range(3):
                            current_piece.rotate()

        # Draw Grid and Tetromino
        draw_grid(screen, grid)
        for y, row in enumerate(current_piece.shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, current_piece.color, 
                                      (current_piece.x * BLOCK_SIZE + x * BLOCK_SIZE,
                                       current_piece.y * BLOCK_SIZE + y * BLOCK_SIZE,
                                       BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()

    print("Game Over! Final Score:", score)
    pygame.quit()

if __name__ == "__main__":
    main()
