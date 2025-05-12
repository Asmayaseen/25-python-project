import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GAME_WIDTH = 10  # SCREEN_WIDTH // BLOCK_SIZE
GAME_HEIGHT = 20  # SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Tetromino Colors
COLORS = [
    (0, 255, 255),  # I - Cyan
    (255, 165, 0),  # O - Orange
    (128, 0, 128),  # T - Purple
    (0, 0, 255),    # J - Blue
    (255, 255, 0),  # L - Yellow
    (0, 255, 0),    # S - Green
    (255, 0, 0),    # Z - Red
]

# Tetromino Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
]

class Tetromino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_idx]
        self.color = COLORS[self.shape_idx]
        self.x = GAME_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self, grid):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        old_shape = self.shape
        self.shape = rotated
        if self.check_collision(grid):
            self.shape = old_shape
            return False
        return True

    def check_collision(self, grid, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if (new_x < 0 or new_x >= GAME_WIDTH or 
                        new_y >= GAME_HEIGHT or 
                        (new_y >= 0 and grid[new_y][new_x] != BLACK)):
                        return True
        return False

def create_grid():
    return [[BLACK for _ in range(GAME_WIDTH)] for _ in range(GAME_HEIGHT)]

def draw_grid(screen, grid):
    for y in range(GAME_HEIGHT):
        for x in range(GAME_WIDTH):
            pygame.draw.rect(screen, grid[y][x], 
                           (x * BLOCK_SIZE, y * BLOCK_SIZE, 
                            BLOCK_SIZE - 1, BLOCK_SIZE - 1))

def merge_tetromino(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell and tetromino.y + y >= 0:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_rows(grid):
    full_rows = [i for i, row in enumerate(grid) if all(cell != BLACK for cell in row)]
    for row_idx in full_rows:
        del grid[row_idx]
        grid.insert(0, [BLACK for _ in range(GAME_WIDTH)])
    return len(full_rows)

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    
    grid = create_grid()
    current_piece = Tetromino()
    next_piece = Tetromino()
    score = 0
    level = 1
    fall_time = 0
    fall_speed = 0.5
    game_over = False
    paused = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                
                if not paused:
                    if event.key == pygame.K_LEFT and not current_piece.check_collision(grid, dx=-1):
                        current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT and not current_piece.check_collision(grid, dx=1):
                        current_piece.x += 1
                    elif event.key == pygame.K_DOWN and not current_piece.check_collision(grid, dy=1):
                        current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        current_piece.rotate(grid)
                    elif event.key == pygame.K_SPACE:
                        while not current_piece.check_collision(grid, dy=1):
                            current_piece.y += 1
                        merge_tetromino(current_piece, grid)
                        rows_cleared = clear_rows(grid)
                        score += rows_cleared * 100 * level
                        level = score // 1000 + 1
                        current_piece = next_piece
                        next_piece = Tetromino()
                        if current_piece.check_collision(grid):
                            game_over = True
                        fall_time = 0

        if paused:
            screen.fill(BLACK)
            draw_text(screen, "PAUSED", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            continue

        fall_time += clock.get_rawtime()
        clock.tick()
        
        if fall_time / 1000 >= fall_speed / level:
            if not current_piece.check_collision(grid, dy=1):
                current_piece.y += 1
            else:
                merge_tetromino(current_piece, grid)
                rows_cleared = clear_rows(grid)
                score += rows_cleared * 100 * level
                level = score // 1000 + 1
                current_piece = next_piece
                next_piece = Tetromino()
                if current_piece.check_collision(grid):
                    game_over = True
            fall_time = 0

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (0, 0, GAME_WIDTH * BLOCK_SIZE, GAME_HEIGHT * BLOCK_SIZE), 1)
        draw_grid(screen, grid)
        
        for y, row in enumerate(current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, current_piece.color, 
                                    ((current_piece.x + x) * BLOCK_SIZE, 
                                     (current_piece.y + y) * BLOCK_SIZE, 
                                     BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        draw_text(screen, f"Score: {score}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        draw_text(screen, f"Level: {level}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        pygame.display.flip()

    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
    draw_text(screen, f"Final Score: {score}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    draw_text(screen, "Press any key to exit", 20, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
    pygame.quit()

if __name__ == "__main__":
    main()