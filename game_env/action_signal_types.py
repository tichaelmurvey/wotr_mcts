from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from game_env.fellowship import Fellowship
    from game_env.game_env_enums import Player
    from game_env.moves.move_types import CardList, MoveType
    from game_env.game_env import WotrGame


from dataclasses import dataclass


@dataclass
class ActionSignal:
    action_type: MoveType
    action_player: Player | None = None
    move_data: None | CardList | Fellowship | WotrGame = None


S = ActionSignal
ActionRequirement = List[ActionSignal]

