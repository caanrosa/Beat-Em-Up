import pygame
import time
from player import Player
from enemy import Enemy
from ciclope_enemy import CyclopeEnemy
from mantis_enemy import MantisEnemy
from background import Background
from camara import Camera
from wave_manager import WaveManager
from score_manager import ScoreManager
import enemy_base

pygame.init()

# CONFIG
score_manager = ScoreManager()

font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)
SCREEN_W, SCREEN_H = 1200, 900
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# RUTAS de las 4 partes del fondo
parts = [
    "assets/escenarios/Part1.png",
    "assets/escenarios/Part2.png",
    "assets/escenarios/Part3.png",
    "assets/escenarios/Part4.png",
]

background = Background(SCREEN_W, SCREEN_H, parts)
camera = Camera(SCREEN_W, SCREEN_H, background.total_width, background.total_height)

# Player
player = Player(300, 350)
player.max_hp = player.hp # guardar vida máxima

# ENEMIGOS 
enemies = pygame.sprite.Group()
e1 = Enemy(1200, 500)
e2 = CyclopeEnemy(1800, 650)
e3 = MantisEnemy(2800, 620)
enemies.add(e1, e2, e3)

# World bounds
world_bounds = (0, background.total_width)
player.world_bounds = world_bounds
for e in enemies:
    e.world_bounds = world_bounds

# WAVES
wave_manager = WaveManager(world_bounds, enemies)

# SCORE_MANAGER y PLAYER_REF
enemy_base.SCORE_MANAGER = score_manager
enemy_base.PLAYER_REF = player

# POPUP / VICTORIA
score_popup_amount = 0
score_popup_timer = 0
SCORE_POPUP_DURATION = 700

won = False
victory_timer = 0
VICTORY_SHOW_TIME = 3500

# Main loop
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Victoria
        if event.type == pygame.USEREVENT + 1:
            won = True
            victory_timer = VICTORY_SHOW_TIME

        # Popup puntaje
        if event.type == pygame.USEREVENT + 2:
            amt = getattr(event, "amount", 0)
            score_popup_amount = amt
            score_popup_timer = SCORE_POPUP_DURATION

    keys = pygame.key.get_pressed()
    player.handle_input(keys, camera)

    # UPDATE
    player.update(dt)
    camera.update(player.rect)

    wave_manager.update(dt, player)

    for enemy in list(enemies):
        enemy.update(dt, player)

    # Colisiones
    for enemy in list(enemies):
        if enemy.is_dead:
            continue

        # Player -> Enemy
        if player.hitbox_active and player.hitbox.colliderect(enemy.hurtbox):
            from_right = player.rect.centerx < enemy.rect.centerx
            enemy.receive_hit(from_right=from_right)

        # Enemy -> Player
        if enemy.hitbox_active and enemy.hitbox.colliderect(player.hurtbox):
            player.receive_hit()

    # Timers
    if score_popup_timer > 0:
        score_popup_timer -= dt
    if won and victory_timer > 0:
        victory_timer -= dt

    # DRAW
    screen.fill((0, 0, 0))

    # Fondo
    background.draw(screen, camera)

    # Player
    px, py = camera.apply_pos(player.rect.x, player.rect.y)
    screen.blit(player.image, (px, py))

    # Enemigos
    for enemy in enemies:
        ex, ey = camera.apply_pos(enemy.rect.x, enemy.rect.y)
        screen.blit(enemy.image, (ex, ey))

    # MARCADOR
    score_text = font.render(f"Score: {score_manager.score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # WAVE
    wave_text = small_font.render(f"Wave: {wave_manager.current_wave}", True, (200, 200, 200))
    screen.blit(wave_text, (20, 70))

   
    # BARRA DE VIDA DEL JUGADOR
    hp_ratio = player.hp / player.max_hp
    bar_x = 20
    bar_y = 120
    bar_w = 250
    bar_h = 25

    # Borde blanco
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 2)

    # Fondo rojo
    pygame.draw.rect(screen, (200, 40, 40), (bar_x, bar_y, bar_w, bar_h))

    # Barra verde (vida)
    inner_w = int(bar_w * hp_ratio)
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, inner_w, bar_h))

    # Popup +score
    if score_popup_timer > 0 and score_popup_amount > 0:
        alpha = int(255 * (score_popup_timer / SCORE_POPUP_DURATION))
        popup_surf = small_font.render(f"+{score_popup_amount}", True, (255, 255, 120))
        popup_surf.set_alpha(alpha)
        screen.blit(popup_surf, (20, 160))

    # Mensaje victoria
    if won:
        v_surf = font.render("YOU WIN!", True, (255, 215, 0))
        vx = (SCREEN_W - v_surf.get_width()) // 2
        vy = (SCREEN_H - v_surf.get_height()) // 2
        screen.blit(v_surf, (vx, vy))

        if victory_timer <= 0:
            running = False

    # GAME OVER
    if player.hp <= 0 and not won:
        go_surf = font.render("GAME OVER", True, (255, 0, 0))
        gx = (SCREEN_W - go_surf.get_width()) // 2
        gy = (SCREEN_H - go_surf.get_height()) // 2
        screen.blit(go_surf, (gx, gy))
        pygame.display.flip()
        pygame.time.delay(2000)

        # Reiniciar juego entero
        player = Player(300, 350)
        player.max_hp = player.hp

        score_manager = ScoreManager()
        wave_manager = WaveManager(world_bounds, enemies)
        enemies.empty()

        # Reiniciar enemigos
        e1 = Enemy(1200, 500)
        e2 = CyclopeEnemy(1800, 650)
        e3 = MantisEnemy(2800, 580)
        enemies.add(e1, e2, e3)

        enemy_base.SCORE_MANAGER = score_manager
        enemy_base.PLAYER_REF = player
        continue
                
    pygame.display.flip()

pygame.quit()
