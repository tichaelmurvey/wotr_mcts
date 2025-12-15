from __future__ import annotations
from enum import IntEnum

class Nation(IntEnum):
    NORTH = 0
    ELVES = 1
    DWARVES = 2
    ROHAN = 3
    GONDOR = 4
    ISENGARD = 5
    MORDOR = 6
    ELINGS = 7


N = Nation


class Player(IntEnum):
    FREE = 0
    SHADOW = 1


P = Player


class GAME_PHASE(IntEnum):
    DRAW_CARDS = 1
    FELLOWSHIP = 2
    HUNT_ALLOCATION = 3
    ACTION_ROLL = 4
    ACTION_RESOLUTION = 5
    VICTORY_CHECK = 6


GP = GAME_PHASE


class TABLE_CARD_TRIGGER(IntEnum):
    HUNT_ROLL = 0
    HUNT_SUCCESS = 1
    HUNT_TILE_IMMINENT = 4
    HUNT_TILE_DRAWN = 2
    HUNT_CASUALTY = 3
    HUNT_DAMAGE = 5
    BEFORE_HUNT_ROLL = 6


TCT = TABLE_CARD_TRIGGER
def get_nation_player(nation: Nation):
    if nation >= Nation.ISENGARD:
        return Player.SHADOW
    else:
        return Player.FREE
