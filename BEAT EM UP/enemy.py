import pygame
from loader import SpriteSheet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.walk_sheet   = SpriteSheet("assets/enemy/walk.png",   "assets/enemy/walk.json")
        self.attack_sheet = SpriteSheet("assets/enemy/attack.png", "assets/enemy/attack.json")

        self.animations = {
            "walk":   self.walk_sheet.get_animation("walk"),
            "attack": self.attack_sheet.get_animation("attack"),
        }

        self.state = "walk"
        self.frame = 0
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        frames = self.animations[self.state]
        self.frame = (self.frame + 0.15) % len(frames)
        self.image = frames[int(self.frame)]
