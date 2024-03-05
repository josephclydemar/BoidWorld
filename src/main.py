import random
import pygame

import summoner
import block

pygame.init()
pygame.display.set_caption('BoidWorld')

WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 750
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont('Serif', 20, bold=True)


do_cohesion = False
do_alignment = False

if __name__ == '__main__':
    myBlocks = (
        block.Block((550, 550), (100, 100), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
        block.Block((350, 450), (20, 500), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
        # block.Block((150, 150), (50, 200), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
        block.Block((760, 200), (800, 50), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
        block.Block((1000, 400), (500, 10), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
        block.Block((900, 620), (30, 250), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
        block.Block((1200, 600), (30, 40), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
        block.Block((420, 400), (30, 40), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
        
        block.Block((1000, 600), (30, 40), (WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW, pygame),
    )
    # myBlocks = []
    mySpawner = summoner.Summoner(
                            [random.randint(10, WINDOW_WIDTH-10), random.randint(10, WINDOW_HEIGHT-10)],
                            myBlocks,
                            (WINDOW_WIDTH, WINDOW_HEIGHT),
                            WINDOW,
                            pygame
                        )
    # boids = mySpawner.myBoids

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        WINDOW.fill((0, 0, 0))

        boid_count_text = FONT.render(f'Boid Count: {len(mySpawner.myBoids)}', False, (255, 255, 255), (0, 0, 0))
        fps_text = FONT.render(f'FPS: {round(CLOCK.get_fps(), 4)}', False, (255, 255, 255), (0, 0, 0))

        
        # my_pos = pygame.mouse.get_pos()
        # my_pos = (my_pos[0], WINDOW_HEIGHT-my_pos[1])

        for blk in myBlocks:
            blk.draw()

        mySpawner.draw(CLOCK.get_fps())
        
        WINDOW.blit(boid_count_text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 60))
        WINDOW.blit(fps_text, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 40))

        pygame.display.update()
        CLOCK.tick(60)