from game_env.army import UNITS_BY_NATION, GenericUnitGroup
from game_env.game_env import WotrGame
from game_env.game_env_enums import Nation, Player
from game_env.moves.move_types import MO, MT, ActionChoice, MoveOption, MusterTarget
from game_env.regions_enum import R


from typing import Dict, List


def define_muster_options(
    game_env: WotrGame,
    player: Player,
) -> List[MoveOption]:
    options: List[MoveOption] = []

    # muster_regions = filter(lambda region: region.can_muster_action(player) , game_env.regions)
    muster_regions = [r for r in game_env.regions if r.can_muster_action(player)]

    # Generate single elite unit options
    for region in muster_regions:
        unit = UNITS_BY_NATION[region.nation][1]  # type: ignore
        options.append(MoveOption(MT.MUSTER, (region.idx, unit, 1)))

    # Generate 2 regular unit options (different settlements)
    all_settlements = [r for regs in muster_regions.values() for r in regs]
    if len(all_settlements) >= 2:
        for i, reg1 in enumerate(all_settlements):
            for reg2 in all_settlements[i + 1 :]:
                move1 = MO(MT.MUSTER, (reg1, "regular", 1))
                move2 = MO(MT.MUSTER, (reg2, "regular", 1))
                options.append((move1, move2))

    # Generate 2 leader options (different settlements)
    for i, reg1 in enumerate(all_settlements):
        for reg2 in all_settlements[i + 1 :]:
            move1 = MO(MT.MUSTER, (reg1, "leader", 1))
            move2 = MO(MT.MUSTER, (reg2, "leader", 1))
            options.append((move1, move2))

    # Generate 1 regular + 1 leader options (different settlements)
    for i, reg1 in enumerate(all_settlements):
        for reg2 in all_settlements:
            if reg1 != reg2:
                move1 = MO(MT.MUSTER, (reg1, "regular", 1))
                move2 = MO(MT.MUSTER, (reg2, "leader", 1))
                options.append((move1, move2))

    return options
