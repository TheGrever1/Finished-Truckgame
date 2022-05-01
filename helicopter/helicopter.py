from random import randrange
import pygame


class Helikopter(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        super().__init__()
        self.image = pygame.image.load("Ressources\heli.png").convert_alpha()
        self.rect = self.image.get_rect(
            midbottom=(-500, 500)
        )  # erste Positon vom Helikopter
        self.position = pygame.math.Vector2(
            (self.rect.x, self.rect.y)
        )  # vector erstellung für unten die Rechnung
        self.speed = (
            2 + difficulty
        )  # pixel per frame + difficulty damit er schneller oder langsamer ist je nach schwierigkeit

    def respawn(self):
        # Random bereich zum spawnen damit der Spieler nicht immer vom gleichen Spawn ausgeht
        self.position = pygame.math.Vector2(
            randrange(-500, 0, 10),
            randrange(300, 1500, 10),
        )

    def move(self, playerpos):
        self.vector_player = pygame.math.Vector2(playerpos)
        # der vektor vom heli schaut wie er sich annähern muss
        self.vector_richtung = (self.vector_player - self.position).normalize()
        # bei beispielsweise heli(10,-30) und spieler(20,-20) dann bewegt er sich (-1,1)
        self.position += self.vector_richtung.elementwise() * self.speed
        self.rect.center = self.position.xy

    def PlayerinArea(self, player_rect):
        """colliderect kontrolliert ob sich 2 rect in einem gleichen bereich sind / berühren

        Args:
            player_rect (rect): Rechteck des spielers

        Returns:
            bool: 1 bei berührung sonst 0
        """
        return self.rect.colliderect(player_rect)
