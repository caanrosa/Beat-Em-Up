import pygame
from player import Player
from enemy import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = Player(200, 500)
        self.all_sprites.add(self.player)

        enemy = Enemy(1000, 500)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.all_sprites.draw(self.screen)
