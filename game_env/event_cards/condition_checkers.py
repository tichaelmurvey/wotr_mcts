
from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from game_env.characters import CompanionName, MinionName
    from game_env.game_env import WotrGame
    from game_env.battle.battle import Battle
    from game_env.army import ArmyUnit


def character_in_play(character : CompanionName | MinionName):
    def _return(game_env: WotrGame):
        character_positions = game_env.minion_pos | game_env.companion_pos
        if character_positions[character] is not None:
            return True
        else:
            return False
    return _return

def units_in_battle(units: Tuple[ArmyUnit, ...]):
    def _return(battle : Battle):
        for unit in units:
            if unit in battle.free_army.units:
                return True
        return False
    return _return