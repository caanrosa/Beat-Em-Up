import pygame

class ScoreManager:
    def __init__(self):
        self.score = 0

        # Lista de milestones que curan al jugador
        self.milestones = [100, 300, 600, 1000, 1500]
        self.milestone_index = 0

        # Para evitar repetir un milestone
        self.completed_milestones = set()

        # SCORE NECESARIO PARA GANAR
        self.WIN_SCORE = 2000
        self.won_triggered = False

    def add_score(self, amount, player):
        """Suma puntaje y chequea milestones y victoria."""
        self.score += amount

        # CHECK DE MILESTONE 
        if (
            self.milestone_index < len(self.milestones)
            and self.score >= self.milestones[self.milestone_index]
        ):
            milestone_value = self.milestones[self.milestone_index]
            self._apply_milestone(player, milestone_value)
            self.milestone_index += 1

        # CHECK DE VICTORIA
        if not self.won_triggered and self.score >= self.WIN_SCORE:
            self.won_triggered = True
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

        return True

    def _apply_milestone(self, player, milestone_value):
        """Aplica curación al jugador al cruzar un milestone."""
        if milestone_value in self.completed_milestones:
            return

        self.completed_milestones.add(milestone_value)

        # CURACIÓN (25% de la vida máxima)
        heal_amount = int(player.max_hp * 0.25)

        # Aplicar curación
        player.hp = min(player.max_hp, player.hp + heal_amount)

        print(f"[MILESTONE] {milestone_value} puntos → +{heal_amount} HP")

        # Evento de popup opcional
        evt = pygame.event.Event(pygame.USEREVENT + 3, {"heal": heal_amount})
        pygame.event.post(evt)
