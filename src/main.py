import random
import pygame

import boids
import spawner

pygame.init()
pygame.display.set_caption('BoidWorld')

WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 750
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont('Serif', 20, bold=True)


do_cohesion = False
do_alignment = False

if __name__ == '__main__':
    mySpawner = spawner.Spawner(
                            [random.randint(10, WINDOW_WIDTH-10), random.randint(10, WINDOW_HEIGHT-10)],
                            (WINDOW_WIDTH, WINDOW_HEIGHT),
                            WINDOW,
                            pygame
                        )
    myBoids = boids.Boid.all_boids
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                
                if event.key == pygame.K_o:
                    for boid in myBoids:
                        boid.do_cohesion = not(boid.do_cohesion)
                if event.key == pygame.K_p:
                    for boid in myBoids:
                        boid.do_alignment = not(boid.do_alignment)
        
        WINDOW.fill((0, 0, 0))

        boid_count_text = FONT.render(f'Boid Count: {len(myBoids)}', False, (255, 255, 255), (0, 0, 0))
        fps_text = FONT.render(f'FPS: {CLOCK.get_fps()}', False, (255, 255, 255), (0, 0, 0))

        my_key = pygame.key.get_pressed()
        # my_pos = pygame.mouse.get_pos()
        # my_pos = (my_pos[0], WINDOW_HEIGHT-my_pos[1])
        
        for boid in myBoids:
            boid.draw(CLOCK.get_fps())
        mySpawner.draw()
        

        if my_key[pygame.K_q]:
            boids.Boid(
                        (mySpawner.position[0], mySpawner.position[1]), 
                        mySpawner,
                        (WINDOW_WIDTH, WINDOW_HEIGHT),
                        WINDOW,
                        pygame,
                        show_circles=False
                    )
        if my_key[pygame.K_w]:
            mySpawner.move()
        if my_key[pygame.K_a]:
            mySpawner.steer(7)
        if my_key[pygame.K_d]:
            mySpawner.steer(-7)

        if my_key[pygame.K_SPACE]:
            mySpawner.burst()
        else:
            mySpawner.relax()
        

        # if my_key[pygame.K_o]:
        #     for boid in myBoids:
        #         boid.do_cohesion = not(boid.do_cohesion)
        # if my_key[pygame.K_p]:
        #     for boid in myBoids:
        #         boid.do_alignment = not(boid.do_alignment)
        
        
        

        WINDOW.blit(boid_count_text, (10, 10))
        WINDOW.blit(fps_text, (10, 40))


        pygame.display.update()
        CLOCK.tick(60)