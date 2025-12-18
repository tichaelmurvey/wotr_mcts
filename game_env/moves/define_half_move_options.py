from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from game_env.army import Army
    from game_env.game_env import WotrGame
    from game_env.game_env_enums import Player
    from game_env.regions.region import Region

from game_env.moves.move_types import MT, MoveOption


# ============================================================================
# OPTION GENERATORS FOR EACH ACTION TYPE
# ============================================================================


def define_half_move_options(
    game_env: WotrGame,
    player: Player,
    requires_leader: bool = False,
    max_armies: int = 2,
) -> List[MoveOption]:
    options: List[MoveOption] = []

    # For each army, find valid destination regions
    for region in game_env.regions:
        region_moves = get_region_march_options(
            game_env, region, player, requires_leader
        )
        if region_moves is not None:
            options += region_moves

    return options


def get_region_march_options(
    game_env: WotrGame,
    region: Region,
    player: Player,
    requires_leader: bool = False,
):

    # see if region has a usable army
    if not region.army:
        return None
    if region.army.player is not player:
        return None
    if requires_leader and region.army.leadership is 0:
        return None

    # check region destinations
    valid_dests = [
        get_valid_march_destination(
            game_env, game_env.regions[adj_region], region.army, player
        )
        for adj_region in region.adj_regions
    ]
    march_options = [
        MoveOption(MT.MOVE_ARMY, (region.idx, dest))
        for dest in valid_dests
        if dest is not None
    ]
    return march_options


def get_valid_march_destination(
    game_env: WotrGame,
    dest: Region,
    army: Army,
    player: Player,
):
    if dest.army and dest.army.player is not player:
        return None

    if dest.nation is not None:
        for unit_nation in army.nations:
            if (unit_nation is not dest.nation) and (
                not game_env.politics.nations[unit_nation].at_war
            ):
                return None  # TODO: Partial unit movement

    return dest.idx
