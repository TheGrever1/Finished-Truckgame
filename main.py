import pygame
from sys import exit
from game import Game

pygame.init()
screen = pygame.display.set_mode((1260, 930))
clock = pygame.time.Clock()
pygame.display.set_caption("Truckspiel")
game = Game(screen, clock)
# In der Main Datei wird Pygame initalisiert und mit pygame Objekte für den screen, die clock und das game angelegt
# Methoden aufruf des Objektes game von der Klasse Game
game.game_loop()
pygame.quit()
exit()
