from enum import Enum

import enum


class Gamestate(enum.Enum):
    # Enum Klasse für die Spiel Zustände
    menu = 0
    playing = 1
    gameover = 2
    gewonnen = 3
    gestrandet = 4
