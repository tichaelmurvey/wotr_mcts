from game_env.army import UNITS_BY_NATION, GenericUnitGroup
from game_env.game_env import WotrGame
from game_env.game_env_enums import Nation, Player
from game_env.moves.move_types import (
    MO,
    MT,
    ActionChoice,
    MoveOption,
    MoveOptionTree,
    MusterTarget,
    OptionBranch,
)
from game_env.regions_enum import R


from typing import Dict, List


def define_muster_options(
    game_env: WotrGame,
    player: Player,
) -> OptionBranch:
    pass
