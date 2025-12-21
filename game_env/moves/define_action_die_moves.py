from __future__ import annotations
from itertools import combinations
from typing import TYPE_CHECKING, Tuple

from game_env.action_signal_types import S
from game_env.game_env import get_opposite_player
from game_env.moves.def_army_die_action import army_die_action_obs

if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from game_env.game_env_enums import Player

from game_env.action_dice.dice import A, ActionResult
from game_env.moves.move_types import (
    MT,
    ADBranch,
    ADChain,
    MoveOption,
    MoveOptionSet,
    MoveOptionTree,
    OptionBranch,
    PassDec,
)


def pass_or_play_opts(move_data: Tuple[WotrGame, Player]) -> MoveOptionSet:
    # check number of dice in pools
    game_env, player = move_data
    pass_opt = MoveOption(MT.PASS_OR_PLAY, PassDec.Pass)
    play_opt = MoveOption(MT.PASS_OR_PLAY, PassDec.Play)

    if len(game_env.player_states[player].dice_pool.get_unused_die_results()) <= len(
        game_env.player_states[
            get_opposite_player(player)
        ].dice_pool.get_unused_die_results()
    ):
        return MoveOptionSet((play_opt,))

    return MoveOptionSet((play_opt, pass_opt))


def exec_pass_or_play(game_env: WotrGame, target: PassDec):
    if target is PassDec.Pass:
        game_env.active_die_player = get_opposite_player(game_env.active_die_player)
    else:
        game_env.move_manager.generate_moves(S(MT.USE_RING))


def use_ring_options(move_data: Tuple[WotrGame, Player]) -> MoveOptionSet:
    game_env, player = move_data
    elven_rings = game_env.player_states[player].elven_rings
    no_ring = MoveOptionSet((MoveOption(MT.USE_RING, False),))
    if elven_rings is 0:
        return no_ring
    if not game_env.player_states[player].dice_pool.is_ring_useful():
        return no_ring
    return MoveOptionSet(
        (MoveOption(MT.USE_RING, False), MoveOption(MT.USE_RING, True))
    )


def exec_use_ring(game_env: WotrGame, target: bool):
    if target:
        game_env.move_manager.generate_moves(S(MT.CHOOSE_CONVERT_DIE))
    else:
        game_env.move_manager.generate_moves(S(MT.CHOOSE_ACTION_DIE))


def choose_die_to_convert_opts(move_data: Tuple[WotrGame, Player]) -> MoveOptionSet:
    game_env, player = move_data
    dicepool = game_env.player_states[player].dice_pool
    active_results = dicepool.get_unused_die_results()
    convertable_dice = filter(lambda result: result is not A.WILL, active_results)
    opts = tuple(MoveOption(MT.CHOOSE_CONVERT_DIE, die) for die in convertable_dice)
    return MoveOptionSet(opts)


def exec_choose_convert_die(game_env: WotrGame, target: ActionResult):
    game_env.converting_die = target
    game_env.move_manager.generate_moves(S(MT.CONVERT_DIE_WITH_RING))


def choose_conversion_result_opts(move_data: Tuple[WotrGame, Player]) -> MoveOptionSet:
    game_env, player = move_data
    conversion_opts = game_env.player_states[player].dice_pool.get_non_available_sides()
    opts = tuple(
        MoveOption(MT.CONVERT_DIE_WITH_RING, result) for result in conversion_opts
    )
    return MoveOptionSet(opts)


def exec_conversion(game_env: WotrGame, target: ActionResult):
    dice = game_env.player_states[game_env.active_die_player].dice_pool.action_dice
    die_to_change = list(
        filter(
            lambda die: (die.action_used is False)
            and (die.current_result is game_env.converting_die),
            dice,
        )
    )[0]
    die_to_change.current_result = target
    if target is A.EYE:
        die_to_change.action_used = True
        game_env.hunt_box.eyes += 1

    game_env.move_manager.generate_moves(S(MT.CHOOSE_ACTION_DIE))


def choose_action_die_opts(move_data: Tuple[WotrGame, Player]) -> MoveOptionSet:
    game_env, player = move_data
    dicepool = game_env.player_states[player].dice_pool
    active_results = dicepool.get_unused_die_results()
    opts = tuple(
        MoveOption(MT.CHOOSE_ACTION_DIE, results) for results in active_results
    )
    return MoveOptionSet(opts)


ACTION_DIE_RESOLVES = {
    A.ARMY: (
        MT.ATTACK,
        MT.DOUBLE_MOVE,
        MT.PLAY_CARD,
        MT.MOVE_ARMY,
    )
}


def exec_choose_action_die(game_env: WotrGame, target: ActionResult) -> MoveOptionSet:
    match target:
        case ActionResult.ARMY:
            pass
        case ActionResult.MUSTER:
            pass
        case ActionResult.HYBRID:
            pass
        case ActionResult.PALANTIR:
            pass
        case ActionResult.CHARACTER:
            pass
        case ActionResult.WILL:
            pass

    return MoveOptionSet(())
