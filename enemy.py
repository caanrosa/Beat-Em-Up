from enemy_base import EnemyBase

class Enemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            walk_png="assets/enemigo/walk.png",
            walk_json="assets/enemigo/walk.json",
            attack_png="assets/enemigo/attack.png",
            attack_json="assets/enemigo/attack.json",
            speed=2.0
        )
