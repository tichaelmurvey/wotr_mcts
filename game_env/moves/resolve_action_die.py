from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, TypedDict

from game_env.game_env_enums import P
from game_env.action_dice.dice import ActionResult
from game_env.action_dice.dice_pool import DicePool
from game_env.characters import CHARACTER_STATS
from game_env.moves.action_generator import ActionOperator
from game_env.moves.move_types import MT, MoveOption, MoveOptionSet
from game_env.regions.region import get_n_regions_away

if TYPE_CHECKING:
    from game_env.fellowship import Fellowship
    from game_env.regions_enum import R
    from game_env.game_env import WotrGame
    from game_env.characters import CompanionName
    from game_env.moves.move_types import MoveTarget

def _action_die_obs(game_env: WotrGame):
    current_player = game_env.active_die_player
    current_dice = game_env.player_states[current_player].dice_pool.action_dice
    action_options = {}
    for die in current_dice:
        


def _action_die_exec(game_env: WotrGame, move_target: MoveTarget):
    pass


resolve_die_operator = ActionOperator(_action_die_obs, _action_die_exec)