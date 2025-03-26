import pygame # type: ignore
import sys
from network import Network

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
 
# Window
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Tic Tac Toe")

# Board
board = [[None] * 3 for _ in range(3)]

# Fonts
font = pygame.font.SysFont(None, 80)

def draw_board():
    win.fill(WHITE)
    for i in range(1, 3):
        pygame.draw.line(win, BLACK, (0, i * HEIGHT // 3), (WIDTH, i * HEIGHT // 3), LINE_WIDTH)
        pygame.draw.line(win, BLACK, (i * WIDTH // 3, 0), (i * WIDTH // 3, HEIGHT), LINE_WIDTH)

def draw_marks():
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                draw_text("X", i, j, RED)
            elif board[i][j] == "O":
                draw_text("O", i, j, BLUE)

def draw_text(text, row, col, color):
    text_surface = font.render(text, True, color)
    win.blit(text_surface, (col * WIDTH // 3 + 60, row * HEIGHT // 3 + 40))

def check_winner():
    # Check Rows and Columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0]:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i]:
            return board[0][i]
    # Check Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]
    return None

def reset_board():
    for i in range(3):
        for j in range(3):
            board[i][j] = None

def main():
    network = Network()
    player = "X" if network.player == 0 else "O"
    print(f"You are Player {player}")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // 200, x // 200

                if board[row][col] is None:
                    board[row][col] = player
                    network.send(f"{row},{col}")

        draw_board()
        draw_marks()

        winner = check_winner()
        if winner:
            print(f"Player {winner} wins!")
            reset_board()

        pygame.display.update()

if __name__ == "__main__":
    main()
