from __future__ import annotations
from collections import namedtuple
from enum import IntEnum
from typing import Dict, Literal, NamedTuple, Required, Tuple, TypedDict, get_args

class CompanionName(IntEnum):
    GANDALF_GREY = 1
    STRIDER = 2
    BOROMIR = 3
    LEGOLAS = 4
    GIMLI = 5
    PIPPIN = 6
    MERRY = 7
    ARAGORN = 8
    GANDALF_WHITE = 9
C = CompanionName

class MinionName(IntEnum):
    WITCH_KING = 10
    MOUTH = 11
    SARUMAN = 12
M = MinionName

class CharacterStats(NamedTuple):
    level: float
    leadership: int
    add_die: bool
    name: str
    abilities: Tuple[str, ...]


class AllCharacterStats(NamedTuple):
    wking: CharacterStats
    mouth: CharacterStats
    saru: CharacterStats
    gandalf_grey: CharacterStats
    gandalf_white: CharacterStats
    strider: CharacterStats
    aragorn: CharacterStats
    legolas: CharacterStats
    boromir: CharacterStats
    gimli: CharacterStats
    merry: CharacterStats
    pippin: CharacterStats


wking = CharacterStats(float("inf"), 2, True, "Witch King", ("smth", "smth else"))
gandalf_white = CharacterStats(4, 2, True, "Gandalf the White", ("shine", "teleport"))

CHARACTER_STATS = AllCharacterStats(
    wking=wking,
    mouth=wking,
    saru=wking,
    gandalf_grey=gandalf_white,
    gandalf_white=gandalf_white,
    strider=gandalf_white,
    aragorn=gandalf_white,
    legolas=gandalf_white,
    boromir=gandalf_white,
    gimli=gandalf_white,
    merry=gandalf_white,
    pippin=gandalf_white,
)
COMPANION_NAMES: tuple[CompanionName, ...] = get_args(CompanionName)
