import pygame
from loader import SpriteSheetLoader

SCORE_MANAGER = None
PLAYER_REF = None

class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, x, y, walk_png, walk_json, attack_png, attack_json, speed=2):
        super().__init__()

        self.animations = {
            "walk_right": SpriteSheetLoader(walk_png, walk_json).get_animation(),
            "walk_left": SpriteSheetLoader(walk_png.replace(".png", "Flip.png"),
                                           walk_json.replace(".json", "Flip.json")).get_animation(),

            "attack_right": SpriteSheetLoader(attack_png, attack_json).get_animation(),
            "attack_left": SpriteSheetLoader(attack_png.replace(".png", "Flip.png"),
                                             attack_json.replace(".json", "Flip.json")).get_animation(),
        }

        self.facing_right = True
        self.state = "walk"
        self.frame = 0

        self.image = self.animations["walk_right"][0].copy()
        self.rect = self.image.get_rect(center=(x, y))

        # HURTBOX 
        self.hurtbox = self.rect.inflate(-30, -20)

        # HITBOX
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.hitbox_active = False

        # MOVIMIENTO / ATAQUE
        self.speed = speed
        self.attack_range = 140
        self.attack_delay = 100
        self.attack_timer = 0

        # VIDA
        self.max_hp = 3
        self.hp = self.max_hp
        self.is_dead = False

        # KNOCKBACK
        self.knockback = 0.0
        self.knockback_speed = 16.0
        self.knockback_friction = 0.86

        # MUERTE
        self.death_timer = 0
        self.world_bounds = None

    def receive_hit(self, from_right=True):
        if self.is_dead:
            return

        self.hp -= 1
        print(f"[ENEMY] HP -> {self.hp}")

        direction = -1 if from_right else 1
        self.knockback = direction * self.knockback_speed
        self.state = "hit"
        self.frame = 0

        if self.hp <= 0:
            self.is_dead = True
            self.death_timer = 600
            self.hitbox_active = False

            try:
                self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
            except:
                pass

            try:
                if SCORE_MANAGER and PLAYER_REF:
                    SCORE_MANAGER.add_score(20, PLAYER_REF)

                    evt = pygame.event.Event(pygame.USEREVENT + 2, {"amount": 20})
                    pygame.event.post(evt)

            except Exception as e:
                print("[SCORE ERROR]", e)

            return

    def update(self, dt, player):

        if self.is_dead:
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.kill()
            return

        # KNOCKBACK
        if abs(self.knockback) > 0.1:
            self.rect.x += int(self.knockback)
            self.knockback *= self.knockback_friction

            if self.world_bounds:
                min_x, max_x = self.world_bounds
                self.rect.x = max(min_x, min(self.rect.x, max_x - self.rect.width))
            return

        dx = player.rect.centerx - self.rect.centerx
        abs_dx = abs(dx)

        # Orientación
        if not (self.state == "attack" and 2 <= self.frame <= 7):
            if abs_dx > 4:
                self.facing_right = dx > 0

        # Estado
        if abs_dx <= self.attack_range and self.state != "attack":
            self.state = "attack"
            self.frame = 0
            self.attack_timer = 0
            self.hitbox_active = False

        elif abs_dx > self.attack_range and self.state != "walk":
            self.state = "walk"
            self.frame = 0
            self.hitbox_active = False

        # Movimiento
        if self.state == "walk":
            direction = 1 if dx > 0 else -1
            self.rect.x += int(direction * self.speed * (dt / 16))

            if self.world_bounds:
                min_x, max_x = self.world_bounds
                self.rect.x = max(min_x, min(self.rect.x, max_x - self.rect.width))

        # Animación
        self.attack_timer += dt
        if self.attack_timer >= self.attack_delay:
            self.attack_timer = 0

            frames = (
                self.animations["walk_right"] if self.facing_right else self.animations["walk_left"]
            ) if self.state == "walk" else (
                self.animations["attack_right"] if self.facing_right else self.animations["attack_left"]
            )

            if not frames:
                return

            self.frame = (self.frame + 1) % len(frames)

            old_bottom = self.rect.bottom
            old_centerx = self.rect.centerx

            self.image = frames[self.frame].copy()
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom
            self.rect.centerx = old_centerx

            # HITBOX
            # HITBOX DEL ATAQUE (
            if self.state == "attack" and 2 <= self.frame <= 7:
                self.hitbox_active = True

                hit_w = 85
                hit_h = 60

                ref = self.hurtbox  # referencia al cuerpo real del enemigo

                if self.facing_right:
                    self.hitbox = pygame.Rect(
                        ref.right,                     # sale de la parte derecha del cuerpo
                        ref.centery - hit_h // 2,      # alineada al torso
                        hit_w,
                        hit_h
                    )
                else:
                    self.hitbox = pygame.Rect(
                        ref.left - hit_w,              # sale de la parte izquierda del cuerpo
                        ref.centery - hit_h // 2,
                        hit_w,
                        hit_h
                    )
            else:
                self.hitbox_active = False
                self.hitbox.size = (0, 0)

        # HURTBOX — centrada correctamente
        self.hurtbox.center = self.rect.center
