import pygame
from loader import SpriteSheetLoader

class Player:
    def __init__(self, x, y):
        # Animaciones
        self.animations = {
            "idle": SpriteSheetLoader(
                "assets/personaje/Reposo.png",
                "assets/personaje/Reposo.json"
            ),
            "walk": SpriteSheetLoader(
                "assets/personaje/Caminata.png",
                "assets/personaje/Caminata.json"
            )
        }

        self.state = "idle"
        self.frame_index = 0
        self.image = self.animations[self.state].get_frame(self.frame_index)

        # Posición
        self.x = x
        self.y = y
        self.speed = 4

        # Reloj interno para la animación
        self.animation_timer = 0
        self.animation_speed = 100  # ms por frame

    def handle_input(self, keys):
        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            moving = True

        if moving:
            self.change_state("walk")
        else:
            self.change_state("idle")

    def change_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.frame_index = 0
            self.animation_timer = 0

    def update(self, dt):
        # Actualizar animación
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % self.animations[self.state].frame_count()

        self.image = self.animations[self.state].get_frame(self.frame_index)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
