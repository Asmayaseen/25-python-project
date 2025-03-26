import pygame # type: ignore
from network import Network

pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Multiplayer Game")
font = pygame.font.SysFont(None, 55)

def draw_text(text, x, y):
    txt_surface = font.render(text, True, (255, 255, 255))
    win.blit(txt_surface, (x, y))

def main():
    run = True
    network = Network()
    player = int(network.get_data())

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        win.fill((30, 30, 30))
        draw_text(f"You are Player {player}", 150, 250)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
