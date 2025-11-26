import pygame
import json
import os

class SpriteSheetLoader:
    def __init__(self, image_path, json_path):
        # Normalizar rutas
        image_path = os.path.abspath(image_path)
        json_path = os.path.abspath(json_path)

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"[ERROR] Imagen no encontrada: {image_path}")

        if not os.path.exists(json_path):
            raise FileNotFoundError(f"[ERROR] JSON no encontrado: {json_path}")

        self.sheet = pygame.image.load(image_path).convert_alpha()

        # Abrir JSON (maneja BOM si existe)
        with open(json_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        self.frames = []

        # Ordenar frames por número (extrae los dígitos en el nombre)
        keys = sorted(
            data["frames"].keys(),
            key=lambda k: int("".join(filter(str.isdigit, k))) if any(ch.isdigit() for ch in k) else 0
        )

        # Extraer frames con pivote corregido
        for key in keys:
            frame_data = data["frames"][key]

            frame = frame_data["frame"]
            sprite_source = frame_data.get("spriteSourceSize", {"x":0, "y":0, "w":frame["w"], "h":frame["h"]})
            source_size = frame_data.get("sourceSize", {"w":frame["w"], "h":frame["h"]})

            # Crear surface del tamaño original del frame
            img = pygame.Surface((source_size["w"], source_size["h"]), pygame.SRCALPHA)

            # Blitear el sprite en la posición correcta dentro del canvas
            img.blit(
                self.sheet,
                (sprite_source["x"], sprite_source["y"]),  # posición en el canvas
                (frame["x"], frame["y"], frame["w"], frame["h"])  # rect del sprite en el sheet
            )

            self.frames.append(img)

    # Para Player
    def get_frame(self, idx):
        return self.frames[idx]

    def frame_count(self):
        return len(self.frames)

    # Para Enemy 
    def get_animation(self):
        return self.frames.copy()
