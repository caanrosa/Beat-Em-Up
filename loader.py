import pygame
import json

class SpriteSheetLoader:
    def __init__(self, image_path, json_path):
        # Cargar spritesheet
        self.spritesheet = pygame.image.load(image_path).convert_alpha()

        # Cargar JSON (soporta BOM)
        with open(json_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        # Los frames vienen como diccionario: { "Idle0000": {...}, "Idle0001": {...} }
        self.frames = []

        for key, frame_data in data["frames"].items():

            frame = frame_data["frame"]
            x = frame["x"]
            y = frame["y"]
            w = frame["w"]
            h = frame["h"]

            # Extraer el frame del spritesheet
            image = self.spritesheet.subsurface(pygame.Rect(x, y, w, h))
            self.frames.append(image)

    def get_frame(self, index):
        return self.frames[index % len(self.frames)]

    def frame_count(self):
        return len(self.frames)
