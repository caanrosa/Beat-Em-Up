from enemy_base import EnemyBase

class CyclopeEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            walk_png="assets/enemigo/ciclopeWalk.png",
            walk_json="assets/enemigo/ciclopeWalk.json",
            attack_png="assets/enemigo/ciclopeAttk.png",
            attack_json="assets/enemigo/ciclopeAttk.json",
            speed=1.6
        )
