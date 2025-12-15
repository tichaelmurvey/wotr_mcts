from __future__ import annotations
import random
from typing import List

from game_env.hunt.hunt_tiles import HuntTile
from game_env.hunt.hunt_data import ALL_HUNT_TILES


class HuntPool:
    tiles: List[HuntTile]
    mordor_addins: List[HuntTile]

    def __init__(self):
        self.tiles = list(filter(lambda tile: tile.special == False, ALL_HUNT_TILES))
        self.mordor_addins = []

    def add_tile(self, tile: HuntTile):
        self.tiles.append(tile)

    def draw_tile(self):
        random.shuffle(self.tiles)
        return self.tiles.pop()

    def discard_tile(self, tile: HuntTile):
        pass

    def remove_tile(self, tile: HuntTile):
        pass
