import pygame

pygame.init()


WINDOW_WIDTH, WINDOW_HEIGHT = 1100, 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


if __name__ == '__main__':
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        WINDOW.fill((0, 0, 0))
        pygame.display.update()