from game_env.army import Army
from game_env.game_env import WotrGame
from game_env.game_env_enums import Player
from game_env.moves.move_types import MO, MT, MoveOption


from typing import List

from game_env.regions.region import Region

# TODO: Partial attack (leaving units behind)


def define_attack_options(
    game_env: WotrGame,
    player: Player,
    requires_leader: bool = False,
):
    options: List[MoveOption] = []
    regions = game_env.regions

    for region in regions:
        region_moves = get_region_attack_options(
            game_env, region, player, requires_leader
        )
        if region_moves is not None:
            options += region_moves

    return options


def get_region_attack_options(
    game_env: WotrGame,
    region: Region,
    player: Player,
    requires_leader: bool = False,
):

    # check if army can attack at all
    if not region.army:
        return None
    if region.army.player is not player:
        return None
    if requires_leader and region.army.leadership is 0:
        return None
    for nation in region.army.nations:
        if not game_env.politics.nations[nation].at_war:
            return None  # TODO: split army attacks

    # check if valid targets exist
    valid_targets = [
        get_valid_attack_targets(game_env.regions[adj_region], player)
        for adj_region in region.adj_regions
    ]

    attack_options = [
        MoveOption(MT.ATTACK, (region.idx, target))
        for target in valid_targets
        if target is not None
    ]

    return attack_options


def get_valid_attack_targets(
    target: Region,
    player: Player,
):
    if target.army is None:
        return None

    if target.army.player is player:
        return None

    return target.idx
