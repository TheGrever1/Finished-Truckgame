import pygame


class Buildings(pygame.sprite.Sprite):
    def __init__(self, imagepth, pos):
        """Initialisierung der Bilder und der Position

        Args:
            imagepth (str): Pfad für die Bild Ressource
            pos (tuple): Feste Position des Gebäudes
        """
        super().__init__()
        self.image = pygame.image.load(imagepth).convert_alpha()
        self.rect = self.image.get_rect(center=(pos))

    def PlayerinArea(self, player_rect):
        """Kontrolle ob Spieler und Gebäude miteinander kollidieren

        Args:
            player_rect (rect): Rechteck des Spielers

        Returns:
            bool: wenn behrührung dann true
        """
        return self.rect.colliderect(player_rect)


class Erzabbaustelle(Buildings):
    def __init__(self):
        super().__init__("Ressources\Erz.png", (100, 500))
        self.maxvorkommen = 500
        self.vorkommen = 500

    def abbauen(self, autolager):
        if self.vorkommen > 0 and autolager < 100:
            self.vorkommen -= 0.2


class Tankstelle(Buildings):
    def __init__(self):
        super().__init__("Ressources\gasstation.png", (800, 50))
        self.type = type
        self.tank = 50000

    def tanken(self, autotankstand):
        if self.tank > 0 and autotankstand < 5000:
            self.tank -= 20


class Erzlager(Buildings):
    def __init__(self):
        super().__init__("Ressources\Warehouse.png", (1000, 800))
        self.type = type
        self.lager = 0

    def lagern(self, autolager):
        if autolager > 0:
            self.lager += 0.2
