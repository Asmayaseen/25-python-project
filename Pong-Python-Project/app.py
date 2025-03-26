import pygame
import time

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 400
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle and Ball Positions
left_paddle = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH-20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_RADIUS, BALL_RADIUS)

# Speeds
ball_speed_x = 4
ball_speed_y = 4

# Scores
left_score = 0
right_score = 0

# Game Loop
def game_loop():
    global ball_speed_x, ball_speed_y, left_score, right_score
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.y -= 5
        if keys[pygame.K_s]:
            left_paddle.y += 5
        if keys[pygame.K_UP]:
            right_paddle.y -= 5
        if keys[pygame.K_DOWN]:
            right_paddle.y += 5

        # Keep paddles in bounds
        left_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle.y))
        right_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle.y))

        # Ball Movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Collision with Walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Collision with Paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1

        # Scoring
        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1
        elif ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1

        # Draw Everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

        # Display Scores
        font = pygame.font.SysFont(None, 50)
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 20))
        screen.blit(right_text, (WIDTH * 3 // 4, 20))

        pygame.display.flip()
        time.sleep(0.02)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
