import pygame
from loader import SpriteSheetLoader

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Animaciones
        self.animations = {
            "idle_right": SpriteSheetLoader("assets/personaje/Reposo.png", "assets/personaje/Reposo.json"),
            "idle_left": SpriteSheetLoader("assets/personaje/ReposoFlip.png", "assets/personaje/ReposoFlip.json"),

            "walk_right": SpriteSheetLoader("assets/personaje/Caminata.png", "assets/personaje/Caminata.json"),
            "walk_left": SpriteSheetLoader("assets/personaje/CaminataFlip.png", "assets/personaje/CaminataFlip.json"),

            "jump_right": SpriteSheetLoader("assets/personaje/Salto.png", "assets/personaje/Salto.json"),
            "jump_left": SpriteSheetLoader("assets/personaje/SaltoFlip.png", "assets/personaje/SaltoFlip.json"),

            "attack_right": SpriteSheetLoader("assets/personaje/AtqNormal.png", "assets/personaje/AtqNormal.json"),
            "attack_left": SpriteSheetLoader("assets/personaje/AtqNormalFlip.png", "assets/personaje/AtqNormalFlip.json"),

            "attack2_right": SpriteSheetLoader("assets/personaje/AtqEspecial.png", "assets/personaje/AtqEspecial.json"),
            "attack2_left": SpriteSheetLoader("assets/personaje/AtqEspecialFlip.png", "assets/personaje/AtqEspecialFlip.json"),

            "hit_right": SpriteSheetLoader("assets/personaje/RecibeDaño.png", "assets/personaje/RecibeDaño.json"),
            "hit_left": SpriteSheetLoader("assets/personaje/RecibeDañoFlip.png", "assets/personaje/RecibeDañoFlip.json"),
        }

        # Estado
        self.state = "idle"
        self.facing_right = True
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 45

        # Imagen inicial
        self.image = self.animations["idle_right"].get_frame(0).copy()
        self.rect = self.image.get_rect(topleft=(x, y))

        # Movimiento
        self.speed = 4
        self.vertical_speed = 0
        self.gravity = 0.6
        self.on_ground = True

        # Hitbox y hurtbox
        self.hurtbox = self.rect.inflate(-40, -20)
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.hitbox_active = False

        # VIDA corregida
        self.max_hp = 5
        self.hp = self.max_hp

        # Invulnerabilidad
        self.invulnerable = False
        self.invul_timer = 0
        self.invul_duration = 900  # ms

        # Límites
        self.world_bounds = None


    # Cambiar estado
    def change_state(self, new):
        if self.state != new:
            self.state = new
            self.frame_index = 0
            self.animation_timer = 0
            self.hitbox_active = False
            self.hitbox.size = (0, 0)

    def handle_input(self, keys, camera=None):

        if self.state == "hit":
            return

        if keys[pygame.K_j]:
            self.change_state("attack")
            return

        if keys[pygame.K_k]:
            self.change_state("attack2")
            return

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vertical_speed = -12
            self.on_ground = False
            self.change_state("jump")
            return

        dx = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.facing_right = True

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.facing_right = False

        self.dx = dx

        if dx != 0:
            self.change_state("walk")
        else:
            self.change_state("idle")

    def receive_hit(self, damage=1):
        if self.invulnerable:
            return

        self.hp -= damage
        print("PLAYER HP =", self.hp)

        self.invulnerable = True
        self.invul_timer = self.invul_duration
        self.change_state("hit")

    def update_invulnerability(self, dt):

        if not self.invulnerable:
            self.image.set_alpha(255)
            return

        self.invul_timer -= dt

        if (self.invul_timer // 80) % 2 == 0:
            self.image.set_alpha(120)
        else:
            self.image.set_alpha(255)

        if self.invul_timer <= 0:
            self.invulnerable = False
            self.image.set_alpha(255)

    def update_hitbox(self):
        if self.state not in ("attack", "attack2"):
            self.hitbox_active = False
            self.hitbox.size = (0, 0)
            return

        if 1 <= self.frame_index <= 6:
            self.hitbox_active = True

            w = 80
            h = 70
            offset_x = 20

            if self.facing_right:
                self.hitbox = pygame.Rect(
                    self.rect.centerx - offset_x,
                    self.rect.centery - h // 2,
                    w, h
                )
            else:
                self.hitbox = pygame.Rect(
                    self.rect.centerx - w + offset_x,
                    self.rect.centery - h // 2,
                    w, h
                )
        else:
            self.hitbox_active = False
            self.hitbox.size = (0, 0)

    def update(self, dt):

        dx = getattr(self, "dx", 0)
        self.rect.x += int(dx * (dt / 16))

        if not self.on_ground:
            self.vertical_speed += self.gravity
            self.rect.y += self.vertical_speed

            ground_y = 750

            if self.rect.bottom >= ground_y:
                self.rect.bottom = ground_y
                self.vertical_speed = 0
                self.on_ground = True
                self.change_state("idle")

        # Animación
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            sheet = self.get_current_animation()
            total = sheet.frame_count()

            self.frame_index = (self.frame_index + 1) % total

            if self.state in ("attack", "attack2", "hit"):
                if self.frame_index == total - 1:
                    self.change_state("idle")

        frame = self.get_current_animation().get_frame(self.frame_index).copy()

        old_bottom = self.rect.bottom
        old_centerx = self.rect.centerx

        self.image = frame
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom
        self.rect.centerx = old_centerx

        # Hitbox / hurtbox
        self.hurtbox.topleft = (self.rect.x + 20, self.rect.y + 10)
        self.update_hitbox()

        # Invulnerabilidad
        self.update_invulnerability(dt)

        # Límites
        if self.world_bounds:
            min_x, max_x = self.world_bounds
            self.rect.x = max(min_x, min(self.rect.x, max_x - self.rect.width))

    def get_current_animation(self):
        direction = "right" if self.facing_right else "left"

        if self.state == "idle":
            return self.animations[f"idle_{direction}"]
        if self.state == "walk":
            return self.animations[f"walk_{direction}"]
        if self.state == "jump":
            return self.animations[f"jump_{direction}"]
        if self.state == "attack":
            return self.animations[f"attack_{direction}"]
        if self.state == "attack2":
            return self.animations[f"attack2_{direction}"]
        if self.state == "hit":
            return self.animations[f"hit_{direction}"]

        return self.animations[f"idle_{direction}"]

    # BARRA DE VIDA DEL JUGADOR
    def draw_health_bar(self, surface, camera=None):

        bar_width = 80
        bar_height = 12

        fill = int((self.hp / self.max_hp) * bar_width)

        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 18

        pygame.draw.rect(surface, (0, 0, 0), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, fill, bar_height))
