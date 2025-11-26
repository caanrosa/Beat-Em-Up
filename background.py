import pygame
import os

class Background:
    def __init__(self, screen_width, screen_height, parts_paths):
        """
        parts_paths: lista de rutas a PNGs en orden (Part1.png, Part2.png...)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Cargar y escalar cada parte al alto de la pantalla
        self.parts = []
        for p in parts_paths:
            path = os.path.abspath(p)
            img = pygame.image.load(path).convert()
            # Escalar para que la altura coincida con screen_height
            scale_factor = screen_height / img.get_height()
            new_w = int(img.get_width() * scale_factor)
            new_h = int(img.get_height() * scale_factor)
            scaled = pygame.transform.scale(img, (new_w, new_h))
            self.parts.append(scaled)

        # Calcular ancho total y alturas uniformes
        self.total_width = sum(img.get_width() for img in self.parts)
        self.total_height = max(img.get_height() for img in self.parts)

    def draw(self, screen, camera):
        """
        Dibuja el fondo teniendo en cuenta camera.offset_x
        """
        x = -camera.offset_x
        for img in self.parts:
            screen.blit(img, (x, 0))
            x += img.get_width()
