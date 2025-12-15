from __future__ import annotations

from dataclasses import dataclass

from game_env.game_env import Player


@dataclass
class HuntTile:
    damage: int = 0
    reveal: bool = False
    stop: bool = False
    eye: bool = False
    special: Player | None = None
    special_action: str | None = None
