import pygame


class AnzeigeMenu:
    def __init__(self):
        self.font = pygame.font.Font(
            None, 25
        )  # Standard schrift, größe 25 font initialisiert

    def text_surf(self, amount, string):
        self.tankfullstand_player_surf = (
            self.font.render(  # surface wird erstellt mit font und text, text farbe
                "%s: %d" % (string, amount), True, "Black"
            )
        )  # dem string wird eine Zahl und ein String übergeben
        return self.tankfullstand_player_surf  # Rückgabe ist ein surface
