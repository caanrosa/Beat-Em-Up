import pygame
from player import Player

pygame.init()
screen = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()

player = Player(400, 300)

running = True
while running:
    dt = clock.tick(60)  # tiempo entre frames

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update(dt)

    screen.fill((50, 50, 50))
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
