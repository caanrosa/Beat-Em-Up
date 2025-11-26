import random
from enemy import Enemy
from ciclope_enemy import CyclopeEnemy
from mantis_enemy import MantisEnemy

class WaveManager:
    def __init__(self, world_bounds, enemies_group):
        self.world_bounds = world_bounds
        self.enemies_group = enemies_group

        self.current_wave = 1
        self.enemies_to_spawn = 3
        self.spawn_cooldown = 350    # más rápido
        self.spawn_timer = 0

        self.wave_active = True
        self.spawned_this_wave = 0   # cantidad real generada

    def update(self, dt, player):
        # Acumular tiempo normal
        self.spawn_timer += dt

        # Comprobación: si todos los enemigos vivos murieron
        alive_enemies = [e for e in self.enemies_group if not e.is_dead]

        if len(alive_enemies) == 0 and self.spawned_this_wave >= self.enemies_to_spawn:
            # Wave terminada
            self.wave_active = False

        # Si wave terminó entonces pasar a nueva wave
        if not self.wave_active:
            self.start_new_wave()
            return

        # Spawn progresivo
        if self.spawned_this_wave < self.enemies_to_spawn:
            if self.spawn_timer >= self.spawn_cooldown:
                self.spawn_enemy(player)
                self.spawn_timer = 0  # reset timer

    def start_new_wave(self):
        self.current_wave += 1
        self.enemies_to_spawn = 2 + self.current_wave
        self.spawned_this_wave = 0
        self.wave_active = True

        print(f"🔥 NUEVA WAVE {self.current_wave} (Enemigos: {self.enemies_to_spawn})")

    def spawn_enemy(self, player):
        """Spawn inteligente basado en posición del jugador."""

        min_x, max_x = self.world_bounds
        px = player.rect.centerx
        safe_distance = 400

        # Lado de spawn
        if random.random() < 0.5:
            spawn_x = random.randint(min_x, px - safe_distance)
        else:
            spawn_x = random.randint(px + safe_distance, max_x - 200)

        # Clamp
        spawn_x = max(min_x, min(spawn_x, max_x - 200))
        spawn_y = random.randint(550, 650)

        # Tipo de enemigo
        enemy_type = random.choices(
            ["enemy", "cyclope", "mantis"],
            weights=[60, 25, 15]
        )[0]

        if enemy_type == "enemy":
            new_enemy = Enemy(spawn_x, spawn_y)
        elif enemy_type == "cyclope":
            new_enemy = CyclopeEnemy(spawn_x, spawn_y)
        else:
            new_enemy = MantisEnemy(spawn_x, spawn_y)

        new_enemy.world_bounds = self.world_bounds
        self.enemies_group.add(new_enemy)

        self.spawned_this_wave += 1

        print(f" → Spawned {enemy_type} en X={spawn_x}")
