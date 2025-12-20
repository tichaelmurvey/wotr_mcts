from collections import Counter
from itertools import chain, combinations, product
from typing import cast
from game_env.game_env_enums import P
from game_env.moves.move_types import MT, CharacterGroupMoveChoice, MoveOption, MoveType
from game_env.regions.region import Region
from game_env.army import AU, Army, GenericUnitGroup, STACK_LIMIT


def define_move_unit_nums(
    region_from: Region, region_to: Region, leader_required: bool = False
) -> list[MoveOption]:
    # Get legal options for which units to move from 1 to 2
    # Check region 2 to avoid exceeding stacking limit
    # Returns all valid combinations of unit types
    if not region_from.army:
        raise Exception("Tried to move from region with no army")

    dest_units = region_to.army.get_unit_count() if region_to.army else 0
    available_space = STACK_LIMIT - dest_units
    if available_space <= 0:
        raise Exception("Tried to move to full region")

    # iterate over armies
    opts: list[GenericUnitGroup] = unit_combinations(region_from.army.units)

    # exclude illegal moves
    moves = [
        MoveOption(MT.CHOOSE_MOVE_GROUP_UNITS, opt)
        for opt in opts
        if validateMovegroupOption(opt, available_space, leader_required)
    ]

    return moves


def define_move_characters_with_army(
    region_from: Region, region_to: Region, player: P, leader_required: bool = False
) -> list[MoveOption]:
    characters = (
        region_from.get_companions() if player is P.FREE else region_from.get_minions()
    )

    if characters is None:
        return []

    characters_required = 1 if leader_required else 0
    return [
        MoveOption(
            MT.CHOOSE_MOVE_GROUP_CHARACTERS,
            cast(CharacterGroupMoveChoice, set(character_set)),
        )
        for character_set in combinations_range(characters, characters_required)
    ]


def validateMovegroupOption(
    opt: GenericUnitGroup, unit_limit: int, ldr_required: bool = False
) -> bool:
    unit_count = Army.calc_unit_count(opt)
    if unit_count == 0:
        return False
    if unit_count > unit_limit:
        return False
    if ldr_required and unit_count < sum(opt.values()):
        return False
    return True


def unit_combinations(counter: Counter) -> list[GenericUnitGroup]:
    """
    Generate all unique combinations of elements up to their counts.
    """

    keys = list(counter.keys())
    ranges = [range(counter[k] + 1) for k in keys]

    groups: list[GenericUnitGroup] = [
        Counter(dict(zip(keys, counts))) for counts in product(*ranges)
    ]
    return groups


def combinations_range(iterable, n1: int = 0, n2: int | None = None):
    if n2 is None:
        n2 = len(iterable)
    """Combinations drawing between n1 and n2 items (inclusive)."""
    return chain.from_iterable(combinations(iterable, r) for r in range(n1, n2 + 1))
