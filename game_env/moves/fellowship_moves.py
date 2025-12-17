from __future__ import annotations
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from game_env.fellowship import Fellowship
    from game_env.regions_enum import R
    from game_env.game_env import WotrGame
    from game_env.characters import CompanionName
from game_env.action_dice.dice import ActionResult
from game_env.action_dice.dice_pool import DicePool
from game_env.characters import CHARACTER_STATS
from game_env.moves.action_generator import ActionOperator
from game_env.moves.move_types import MT, MoveOption, MoveOptionSet
from game_env.regions.region import get_n_regions_away


def define_options_declare(fellowship : Fellowship):
    dest_options = tuple(MoveOption(MT.DECLARE_FELLOWSHIP, region) for region in get_n_regions_away(fellowship.region.idx, fellowship.track_position, fellowship.regions))

    return MoveOptionSet(dest_options)


def execute_action_declare(game_env: WotrGame, move_target: R):
    game_env.fellowship.declare(move_target)


def define_options_guide(fellowship : Fellowship):
    highest_level = max(CHARACTER_STATS[companion].level for companion in fellowship.companions)
    options = tuple(MoveOption(MT.CHANGE_GUIDE, companion) for companion in fellowship.companions if CHARACTER_STATS[companion].level == highest_level)
    return MoveOptionSet(options)
    

def execute_action_guide(game_env: WotrGame, move_target: CompanionName):
    game_env.fellowship.change_guide(move_target)

def define_options_hunt_allocation(game_env : WotrGame):
    num_shadow_dice = len(game_env.player_state_shadow.dice_pool.action_dice)
    num_companions = len(game_env.fellowship.companions)
    moved_last_turn = game_env.fellowship.moved_last_turn
    min_eyes = 1 if moved_last_turn else 0
    max_eyes = min(num_companions, num_shadow_dice)
    options = tuple(MoveOption(MT.HUNT_ALLOCATION, num) for num in range(min_eyes, max_eyes))
    return MoveOptionSet(options)


def execute_action_hunt_allocation(game_env: WotrGame, move_target: int):
    eye_dice = game_env.player_state_shadow.dice_pool.action_dice[:move_target]
    for die in eye_dice:
        die.current_result = ActionResult.EYE
        die.action_used = True
    game_env.hunt_box.eyes = move_target