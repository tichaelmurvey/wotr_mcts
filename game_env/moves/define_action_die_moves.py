from __future__ import annotations
from typing import TYPE_CHECKING

from game_env.moves.def_army_die_action import army_die_action_obs

if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from game_env.game_env_enums import Player

from game_env.action_dice.dice import ActionResult
from game_env.moves.move_types import (
    ADBranch,
    ADChain,
    MoveOptionTree,
    OptionBranch,
    PassDec,
)


def define_action_die_moves(game_env: WotrGame, player: Player) -> ADBranch:
    active_dice = game_env.player_states[player].dice_pool.get_unused_die_results()

    move_tree = ADBranch(None, [])

    # pass or play
    move_tree.opts.append(ADBranch(PassDec.Pass, []))

    play_die = ADBranch(PassDec.Play, [])

    for die in active_dice:
        match die:
            case ActionResult.ARMY:
                play_die.opts.append(
                    army_die_action_obs(
                        game_env,
                        player,
                    )
                )

            case ActionResult.MUSTER:
                pass
            case ActionResult.PALANTIR:
                pass
            case ActionResult.ARMY:
                pass
            case ActionResult.HYBRID:
                pass
            case ActionResult.WILL:
                pass

    return move_tree
