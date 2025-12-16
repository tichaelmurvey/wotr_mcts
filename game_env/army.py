from __future__ import annotations
from collections import Counter
from enum import IntEnum
from typing import NamedTuple, cast
from game_env.characters import CHARACTER_STATS, CompanionName, MinionName
from game_env.game_env_enums import P

class FreeUnit(IntEnum):
    nort_reg = 0
    nort_elt = 1
    nort_ldr = 2
    elvn_reg = 3
    elvn_elt = 4
    elvn_ldr = 5
    dwar_reg = 6
    dwar_elt = 7
    dwar_ldr = 8
    rohn_reg = 9
    rohn_elt = 10
    rohn_ldr = 11
    gond_reg = 12
    gond_elt = 13
    gond_ldr = 14

FU = FreeUnit

class ShadowUnit(IntEnum):
    isen_reg = 15
    isen_elt = 16
    mord_reg = 17
    mord_elt = 18
    east_reg = 19
    east_elt = 20
    nazgul = 21

SU = ShadowUnit

class ArmyUnit(IntEnum):
    nort_reg = 0
    nort_elt = 1
    nort_ldr = 2
    elvn_reg = 3
    elvn_elt = 4
    elvn_ldr = 5
    dwar_reg = 6
    dwar_elt = 7
    dwar_ldr = 8
    rohn_reg = 9
    rohn_elt = 10
    rohn_ldr = 11
    gond_reg = 12
    gond_elt = 13
    gond_ldr = 14
    isen_reg = 15
    isen_elt = 16
    mord_reg = 17
    mord_elt = 18
    east_reg = 19
    east_elt = 20
    nazgul = 21

AU = ArmyUnit

UnitGroupShadow = Counter[ShadowUnit]
UnitGroupFree = Counter[FreeUnit]

type UnitGroup = UnitGroupShadow | UnitGroupFree
type GenericUnitGroup = Counter[ArmyUnit]

class ArmyStats(NamedTuple):
    strength: int
    leadership: int


SHADOW_KEYS = {
    "isen_reg",
    "isen_elt",
    "mord_reg",
    "mord_elt",
    "east_reg",
    "east_elt",
}


def get_unit_group_player(units: UnitGroup):
    x = {x.name for x in units.keys()}
    return P.SHADOW if x & SHADOW_KEYS else P.FREE


class Army:
    units: Counter[ShadowUnit] | Counter[FreeUnit]

    def __init__(
        self,
        units: Counter[ShadowUnit] | Counter[FreeUnit],
        minions: set[MinionName] | None = None,
        companions: set[CompanionName] | None = None,
        nazgul: int = 0,
    ):
        self.units = units
        self.player = get_unit_group_player(units)
        self.minions = minions
        self.companions = companions
        self.nazgul = nazgul
        self.strength = 0
        self.leadership = 0

    def get_stats(self):
        return ArmyStats(self.strength, self.leadership)

    def calc_stats(self):
        strength = 0
        leadership = 0
        for unit, count in self.units.items():
            if unit.name.endswith("_reg"):
                strength += count
            elif unit.name.endswith("_elt"):
                strength += count * 2
            elif unit.name.endswith("_ldr"):
                leadership += count

        if self.minions:
            for name in self.minions:
                leadership += CHARACTER_STATS[name].leadership

        if self.companions:
            for name in self.companions:
                leadership += CHARACTER_STATS[name].leadership

        leadership += self.nazgul

        self.strength, self.leadership = strength, leadership

    def get_unit_count(self) -> int:
        total = 0
        for unit, count in self.units.items():
            if not unit.name.endswith("_ldr"):
                total += cast(int, count)
        return total
