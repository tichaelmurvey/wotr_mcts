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
    name: str
    abilities: Tuple[str, ...]
    add_die: bool = False

wking = CharacterStats(float("inf"), 2, "Witch King", ("smth", "smth else"), True)
saruman = CharacterStats(float("inf"), 2, "Witch King", ("smth", "smth else"), True)
mouth = CharacterStats(float("inf"), 2, "Witch King", ("smth", "smth else"), True)
gandalf_white = CharacterStats(4, 2, "Gandalf the White", ("shine", "teleport"), True)
aragorn = CharacterStats(4, 2, "Aragorn", ("shine", "teleport"), True)
gandalf_grey = CharacterStats(3, 2, "Gandalf the Grey", ("shine", "teleport"))
strider = CharacterStats(3, 1, "Gandalf the White", ("shine", "teleport"))
boromir = CharacterStats(2, 1, "Gandalf the White", ("shine", "teleport"))
legolas = CharacterStats(2, 1, "Gandalf the White", ("shine", "teleport"))
gimli = CharacterStats(2, 1, "Gandalf the White", ("shine", "teleport"))
merry = CharacterStats(1, 1, "Gandalf the White", ("shine", "teleport"))
pippin = CharacterStats(1, 1, "Gandalf the White", ("shine", "teleport"))

CHARACTER_STATS: dict[CompanionName | MinionName, CharacterStats] = {
    C.GANDALF_GREY: gandalf_grey,
    C.STRIDER: strider,
    C.BOROMIR: boromir,
    C.LEGOLAS: legolas,
    C.GIMLI: gimli,
    C.PIPPIN: pippin,
    C.MERRY: merry,
    C.ARAGORN: aragorn,
    C.GANDALF_WHITE: gandalf_white,
    M.WITCH_KING: wking,
    M.MOUTH: mouth,
    M.SARUMAN: saruman,
}

COMPANION_NAMES: tuple[CompanionName, ...] = tuple(CompanionName)
MINION_NAMES: tuple[MinionName, ...] = tuple(MinionName)