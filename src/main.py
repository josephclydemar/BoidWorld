import pygame
import boids

pygame.init()


WINDOW_WIDTH, WINDOW_HEIGHT = 1100, 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

if __name__ == '__main__':
    myBoids = [boids.Boid((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame) for _ in range(5000)]
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        WINDOW.fill((0, 0, 0))
        for boid in myBoids:
            boid.draw()
            boid.move((500, 300))
        pygame.display.update()
        CLOCK.tick(120)