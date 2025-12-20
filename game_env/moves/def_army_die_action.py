from game_env.action_dice.dice import A, ActionResult
from game_env.game_env import WotrGame
from game_env.game_env_enums import Player
from game_env.moves.move_types import ADBranch, ADResolve, OptionBranch
from game_env.regions_enum import R


def army_die_action_obs(game_env: WotrGame, player: Player) -> ADBranch:
    play_army = ADBranch(A.ARMY, [])

    play_army.opts.append(double_move_opts(game_env, player))

    return play_army


def double_move_opts(game_env: WotrGame, player: Player) -> ADBranch:
    double_move = ADBranch(ADResolve.DOUBLE_MOVE, [])

    return double_move
