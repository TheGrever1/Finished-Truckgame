import pygame


class Player(pygame.sprite.Sprite):
    # Spieler Klasse für Steuerung und Logik bei Collision

    def __init__(self):
        """Initialsierung  des Spielers
        Image bekommt das Bild zugewiesen und es setzt
        das Pixel Format auf das vom Bildschirm und versteckt alpha pixel (png transparenz wenn vorhanden)

        Dann wird ein Rechteck angelegt und bekommt eine Position auf dieser der SPieler dann später spawnt

        Das start lager und Tankfüllstand wird angelegt
        """
        super().__init__()
        self.image = pygame.image.load("Ressources\car-truck4.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.tankfullstand = 2000
        self.lager = 0

    def player_input(self):
        """Kümmert sich um bewegung und Verbrauch des treibstoffes"""
        info = pygame.display.Info()
        if self.tankfullstand > 0:
            # key.get_pressed() liefert eine Liste mit den Keys zurück gedrückte sind 1 und nicht gedrückte 0
            keys = pygame.key.get_pressed()
            playerspeed = 3
            y_change = 0
            x_change = 0
            if keys[pygame.K_w] and keys[pygame.K_a]:
                y_change = -playerspeed
                x_change = -playerspeed
            if keys[pygame.K_w] and keys[pygame.K_d]:
                y_change = -playerspeed
                x_change = playerspeed
            if keys[pygame.K_w]:
                y_change = -playerspeed
            if keys[pygame.K_s] and keys[pygame.K_a]:
                y_change = playerspeed
                x_change = -playerspeed
            if keys[pygame.K_s] and keys[pygame.K_d]:
                y_change = playerspeed
                x_change = playerspeed
            if keys[pygame.K_s]:
                y_change = playerspeed
            if keys[pygame.K_d]:
                x_change += playerspeed
            if keys[pygame.K_a]:
                x_change = -playerspeed

            if (
                # wenn sich der spieler bewegt wird verbrauch aufgerufen und damit tank verbraucht
                keys[pygame.K_s]
                or keys[pygame.K_d]
                or keys[pygame.K_w]
                or keys[pygame.K_a]
            ):
                self.verbrauch()

            self.rect.x += x_change
            self.rect.y += y_change

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > info.current_h:
                self.rect.bottom = info.current_h
            if self.rect.right > info.current_w:
                self.rect.right = info.current_w

    def tanken(self):
        if self.tankfullstand <= 5000:
            # kontrolle ob in denk tank noch 20 "liter" passen
            if (self.tankfullstand + 20) > 5000:
                # wenn nicht wird der rest nur getankt bspw tankfullstand = 4991
                self.tankfullstand -= 5000 - self.tankfullstand
            else:  # 4991 + 20 ist größer als 5000 die differenz ist 9 heißt also
                self.tankfullstand += 20  # es passen also nur noch 9 rein

    def verbrauch(self):
        if self.tankfullstand > 0:
            self.tankfullstand -= 5

    def abbauen(self, erzlagerkapa):
        # solang der erzvorrat reicht und der truck nicht voll ist kann aufgeladen werden
        if self.lager < 100 and erzlagerkapa >= 0:
            self.lager += 0.2

    def lagern(self):
        if self.lager > 0:
            self.lager -= 0.2

    def wareverloren(self):
        self.lager = 0

    def check_border(self):
        if self.rect.left < 0:
            pass
        if self.rect.top < 0:
            pass
        if self.rect.bottom > self.info.current_h:
            pass
        if self.rect.right > self.info.current_w:
            pass

    def update(self):
        self.player_input()
