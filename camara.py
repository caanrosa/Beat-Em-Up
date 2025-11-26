class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height=0):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height

        self.offset_x = 0
        self.offset_y = 0

    def update(self, target_rect):
        # centrar horizontalmente al jugador 
        target_x = target_rect.centerx - self.screen_width // 2
        target_y = target_rect.centery - self.screen_height // 2

        # Clamp dentro de mundo
        max_x = max(0, self.world_width - self.screen_width)
        max_y = max(0, self.world_height - self.screen_height)

        self.offset_x = max(0, min(int(target_x), max_x))
        self.offset_y = max(0, min(int(target_y), max_y))

    def apply_pos(self, world_x, world_y):
        """Devuelve las coordenadas de pantalla para una posición del mundo."""
        return world_x - self.offset_x, world_y - self.offset_y
