import random

import pygame
import boids

pygame.init()
pygame.display.set_caption('BoidWorld')

WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 750
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont('Serif', 25, bold=True)



if __name__ == '__main__':
    myBoids = [boids.Boid(
                            [random.randint(10, WINDOW_WIDTH-10), random.randint(10, WINDOW_HEIGHT-10)],
                            (WINDOW_WIDTH, WINDOW_HEIGHT),
                            WINDOW,
                            pygame,
                            show_circles=False
                        ) for _ in range(100)]
    for boid in myBoids:
        boid.get_neigbors(list(map(lambda b: b.position, list(filter(lambda b: b != boid, myBoids)))))
    run = True
    while run:
        pygame.display.update()
        CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        WINDOW.fill((0, 0, 0))
        boid_count_text = FONT.render(f'Boid Count: {len(myBoids)}', False, (255, 255, 255), (0, 0, 0))
        fps_text = FONT.render(f'FPS: {CLOCK.get_fps()}', False, (255, 255, 255), (0, 0, 0))
        

        # my_key = pygame.key.get_pressed()
        # # print(my_key[pygame.K_SPACE])
        # my_pos = pygame.mouse.get_pos()
        # my_pos = (my_pos[0], WINDOW_HEIGHT-my_pos[1])
        for boid in myBoids:
            boid.draw(CLOCK.get_fps())
            # boid.move(my_pos)
        # if my_key[pygame.K_SPACE]:
        #     myBoids.append(boids.Boid(my_pos,(WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame))
        # if random.randint(500, 1000) % random.randint(100, 499) == 0:
        #     myBoids.append(boids.Boid((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame))
        #     myBoids += [boids.Boid((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame) for _ in range(10)]
        #     my_pos = (random.randint(100, WINDOW_WIDTH-100), random.randint(100, WINDOW_HEIGHT-100))
        
        WINDOW.blit(boid_count_text, (10, 10))
        WINDOW.blit(fps_text, (10, 40))