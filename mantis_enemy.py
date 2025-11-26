from enemy_base import EnemyBase

class MantisEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            walk_png="assets/enemigo/mantisWalk.png",
            walk_json="assets/enemigo/mantisWalk.json",
            attack_png="assets/enemigo/mantisAttk.png",
            attack_json="assets/enemigo/mantisAttk.json",
            speed=2.5
        )
