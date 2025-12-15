from __future__ import annotations
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from game_env.fellowship import Fellowship
    from game_env.regions_enum import R
    from game_env.game_env import WotrGame
    from game_env.characters import CompanionName
from game_env.characters import CHARACTER_STATS
from game_env.moves.action_generator import ActionOperator
from game_env.moves.move_types import MT, MoveOption, MoveOptionSet
from game_env.regions.region import get_n_regions_away


def _define_options_declare(fellowship : Fellowship):
    dest_options = tuple(set(MoveOption(MT.DECLARE_FELLOWSHIP, region) for region in get_n_regions_away(fellowship.region.idx, fellowship.track_position, fellowship.regions)))

    return MoveOptionSet(dest_options)


def _execute_action_declare(game_env: WotrGame, move_target: R):
    game_env.fellowship.declare(move_target)


declare_operator = ActionOperator(_define_options_declare, _execute_action_declare)

def _define_options_guide(fellowship : Fellowship):
    highest_level = max(CHARACTER_STATS[companion].level for companion in fellowship.companions)
    options = tuple(MoveOption(MT.CHANGE_GUIDE, companion) for companion in fellowship.companions if CHARACTER_STATS[companion].level == highest_level)
    return MoveOptionSet(options)
    

def _execute_action_guide(game_env: WotrGame, move_target: CompanionName):
    game_env.fellowship.change_guide(move_target)


change_guide_operator = ActionOperator(_define_options_guide, _execute_action_guide)