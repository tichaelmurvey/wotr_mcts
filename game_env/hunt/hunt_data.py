from __future__ import annotations
from typing import List
from game_env.game_env import Player
from game_env.hunt.hunt_tiles import HuntTile


tile = HuntTile(damage=1, reveal=True)
blue_tile = HuntTile(damage=-1, special=Player.FREE)
red_tile = HuntTile(special=Player.SHADOW, special_action="shelob", stop=True)

ALL_HUNT_TILES: List[HuntTile] = [tile] * 20 + [blue_tile] * 4 + [red_tile] * 4
