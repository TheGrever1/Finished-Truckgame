import pygame
import pygame_menu
from Map.Anzeige import AnzeigeMenu
from Map.buildings import Erzabbaustelle
from Map.buildings import Erzlager
from Map.buildings import Tankstelle
from player.Player import Player
from gamestate import Gamestate
from helicopter.helicopter import Helikopter


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        # standard schwierigkeit
        self.schwierigkeit = 1
        self.menu("Wilkommen")

    def game_loop(self):
        self.helicopter = Helikopter(self.schwierigkeit)
        self.tankstelle = Tankstelle()
        self.erzabbauch = Erzabbaustelle()
        self.erzlager = Erzlager()
        self.player_usage = Player()
        self.screen = pygame.display.set_mode((1260, 930))
        gamestate = Gamestate.playing
        self.player = pygame.sprite.GroupSingle()
        object_group = pygame.sprite.Group()
        menu_surfaces = AnzeigeMenu()
        # Hier werden am anfang alle Objekte initialsiert und nicht in der init
        # da sie sich sonst nicht resetten würden wenn man nach einem lose wieder
        # spielen möchte und sonst hätte man redudanten code
        self.player.add(self.player_usage)
        # für den spieler gibt es aber eine extra gruppe sie ist eine GroupSingle und kann nur einmal existieren
        object_group.add(self.tankstelle)
        object_group.add(self.erzabbauch)
        object_group.add(self.erzlager)
        object_group.add(self.helicopter)
        # Pygame bietet gruppen an für sprites mit denen man leicht
        # eine anzahl an sprites aktuallisieren kann und malen (draw())

        while gamestate == Gamestate.playing:

            for event in pygame.event.get():
                # wenn der user das fenster schließt während dem spiel wird er gamestate auf menu gestellt und es öffnet sich das menu
                if event.type == pygame.QUIT:
                    gamestate = Gamestate.menu
                # bei leerem tank wird der spielstand auf gestrandet gesetzt und es ist gameover es öffnet sich ebenso das menu
                if self.player_usage.tankfullstand == 0:
                    gamestate = Gamestate.gestrandet
            if (
                self.player_usage.lager
                + self.erzabbauch.vorkommen
                + self.erzlager.lager
            ) <= (self.erzabbauch.maxvorkommen / 100) * 80:
                gamestate = Gamestate.gameover
                # wenn bereits 20% von den Erzen geklaut wurden ist das spiel verloren
            elif (self.erzlager.lager) >= (self.erzabbauch.maxvorkommen / 100) * 80:
                gamestate = Gamestate.gewonnen

            self.collision_sprite()  # aufruf der Collision Methode
            self.helicopter.move(self.player_usage.rect.center)
            self.screen.fill((255, 255, 255))  # Screen wird Weiß gefärbt
            object_group.draw(self.screen)  # Alle sprites in der Gruppe werden gemalt
            object_group.update()  # Alle Sprite Update Methoden werden aufgerufen
            self.player.draw(self.screen)  # Spieler wird gemalt
            self.player.update()  # spieler update methode wird aufgerufen
            self.screen.blit(
                menu_surfaces.text_surf(self.player_usage.tankfullstand, "Tank"),
                (10, 800),
            )
            self.screen.blit(
                menu_surfaces.text_surf(self.tankstelle.tank, "Tankstelle"),
                (10, 825),
            )
            self.screen.blit(
                menu_surfaces.text_surf(
                    self.player_usage.lager, "Lager"
                ),  # Blit malt alle Bild auf bild und somit werden alle text surfaces hier auf den screen gemalt
                (10, 850),
            )
            self.screen.blit(
                menu_surfaces.text_surf(self.erzabbauch.vorkommen, "Erzquelle"),
                (10, 875),
            )
            self.screen.blit(
                menu_surfaces.text_surf(self.erzlager.lager, "Warehouselager"),
                (10, 900),
            )
            pygame.display.update()
            self.clock.tick(60)
            # clock wird 60 übergeben heißt das spiel läuft mit 60 ticks die sekunde
        if gamestate == Gamestate.gameover:
            self.menu("Verloren")
        if gamestate == Gamestate.menu:
            self.menu("Wilkommen")
        if gamestate == Gamestate.gewonnen:
            self.menu("Gewonnen!")
        if gamestate == Gamestate.gestrandet:
            self.menu("Gestrandet")

    def collision_sprite(self):
        # Spieler Rechteck wird übergeben und in der Methode Playerinarea wird geschaut ob diese zwei kollidieren
        if self.tankstelle.PlayerinArea(self.player_usage.rect):
            self.tankstelle.tanken(self.player_usage.tankfullstand)
            self.player_usage.tanken()  # Methoden aufruf für Aktion die benötigt wird
        if self.erzabbauch.PlayerinArea(self.player_usage.rect):
            self.player_usage.abbauen(self.erzabbauch.vorkommen)
            self.erzabbauch.abbauen(self.player_usage.lager)
        if self.erzlager.PlayerinArea(self.player_usage.rect):
            self.erzlager.lagern(self.player_usage.lager)
            self.player_usage.lagern()
        if self.helicopter.PlayerinArea(self.player_usage.rect):
            self.helicopter.respawn()
            self.player_usage.wareverloren()

    def menu(self, text):
        self.screen = pygame.display.set_mode((400, 300))
        menu = pygame_menu.Menu(
            "Transporter", 400, 300, theme=pygame_menu.themes.THEME_DARK
        )

        menu.add.label(text)  # Menü Einstellung Design,Labels,Buttons
        menu.add.selector(
            "Difficulty :", [("Easy", 1), ("Hard", 2)], onchange=self.set_difficulty
        )
        menu.add.button("Play", self.game_loop)
        menu.add.button("Quit", pygame_menu.events.EXIT)
        menu.mainloop(self.screen)
        # Screen übergabe damit das menü auf den Screen gemalt wird

    def set_difficulty(self, _, difficulty):
        self.schwierigkeit = difficulty
