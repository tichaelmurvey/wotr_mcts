from typing import Tuple
from game_env.action_dice.dice import A, ActionResult
from game_env.game_env import WotrGame
from game_env.game_env_enums import P, Player
from game_env.moves.move_types import (
    MT,
    ADBranch,
    ADResolve,
    MoveOption,
    MoveOptionSet,
    OptionBranch,
    ResolutionOption,
)
from game_env.regions_enum import R

def die_resolution_opts(move_data: Tuple[WotrGame, Player, ActionResult]) -> MoveOptionSet:
    resolves = get_resolves(move_data)

    opts = tuple(
        MoveOption(MT.CHOOSE_DIE_RESOLUTION, (A.ARMY, resolve)) for resolve in resolves
    )

    return MoveOptionSet(opts)

def get_resolves(move_data: Tuple[WotrGame, Player, ActionResult]):
    game_env, player, action_result = move_data
    
    

    match action_result:
        case A.ARMY:
            return (
                MT.ATTACK,
                MT.DOUBLE_MOVE,
                MT.PLAY_CARD,
                MT.MOVE_ARMY,
            )
        case A.MUSTER:
            if player is P.FREE:
                return (
                    MT.MUSTER,
                    MT.ADVANCE_NATION_POLITICS,
                    MT.
                )
    

def exec_die_resolution(game_env: WotrGame, move_target: ResolutionOption):



def army_die_action_obs(game_env: WotrGame, player: Player) -> ADBranch:
    play_army = ADBranch(A.ARMY, [])

    play_army.opts.append(double_move_opts(game_env, player))

    return play_army


def double_move_opts(game_env: WotrGame, player: Player) -> ADBranch:
    double_move = ADBranch(ADResolve.DOUBLE_MOVE, [])

    return double_move
