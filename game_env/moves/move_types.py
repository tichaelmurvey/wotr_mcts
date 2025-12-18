"""
Move types
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, List, NamedTuple, Tuple, Any
from enum import IntEnum
from dataclasses import dataclass

if TYPE_CHECKING:
    from game_env.characters import CompanionName, MinionName
    from game_env.regions_enum import R
    from game_env.game_env import WotrGame
    from game_env.game_env_enums import Nation, Player
    from game_env.event_cards.cards import DeckType, EventCard
    from game_env.army import AU


class OptsPolicy(IntEnum):
    FLAT = 0
    INDEPENDENT_SEQUENCE = 1
    DEPENDENT_TREE = 2


class MoveType(IntEnum):
    EVENT_CARD_DISCARD = 0
    RESOLVE_ACTION_DIE = 1
    CHOOSE_COMBAT_CARD = 2
    CHANGE_GUIDE = 3
    RESOLVE_HUNT_DAMAGE = 4
    DECLARE_FELLOWSHIP = 5
    REVEAL_FELLOWSHIP = 6
    USE_HUNT_TABLE_CARD = 7
    USE_GUIDE_HUNT_ABILITY = 8
    SHADOWS_GATHER = 9
    HUNT_ALLOCATION = 10

    # Dice resolutions
    MOVE_ARMY = 11
    MOVE_COMPANIONS = 12
    MOVE_MINIONS = 13
    MUSTER = 14
    ATTACK = 15
    PLAY_CARD = 16
    DRAW_CARD = 17
    MOVE_FELLOWSHIP = 18
    HIDE_FELLOWSHIP = 19
    SEPARATE_COMPANIONS = 20
    ADVANCE_NATION_POLITICS = 21
    RECRUIT_MINION = 22
    RECRUIT_DICE_COMPANION = 23
    PASS = 24

    # special dice actions
    CONVERT_FROM_WOTW = 30
    CONVERT_TO_EYE = 25
    CONVERT_TO_WOTW = 26
    KILL_WOTW = 27
    USE_RING_FP = 28
    USE_RING_SP = 29


MT = MoveType


@dataclass
class CardReference:
    player: Player
    deck: DeckType
    idx: int


class March(NamedTuple):
    src: R
    dest: R


type MusterTarget = Tuple[R, AU, int]

type MoveTarget = (
    None
    | CardReference
    | R
    | CompanionName
    | MinionName
    | Nation
    | March
    | int
    | str
    | Tuple[R, R]
    | Tuple[R, str, int]
    | Tuple[R, CompanionName]
    | Tuple[str, R]
    | Tuple[MinionName, R]
    | Tuple[MinionName, None]
    | MusterTarget
)


@dataclass
class MoveOption:
    move_type: MoveType
    move_target: MoveTarget


MO = MoveOption


@dataclass
class MoveOptionSet:
    options: Tuple[MoveOption, ...]
    num_to_choose: int = 1
    policy: OptsPolicy = OptsPolicy.FLAT


MOS = MoveOptionSet


@dataclass
class OptionBranch:
    this_step_choice: MoveOption
    next_step_options: list[OptionBranch] | None


@dataclass
class MoveOptionTree:
    option_branches: list[OptionBranch]
    shared_state: Any = ""


ActionChoice = Tuple[
    MoveOption, ...
]  # action choice is one move, or a sequence of non-interrupted moves

ActionChoiceSet = Tuple[ActionChoice, ...]


@dataclass
class ActionSpace:
    action_set: ActionChoiceSet
    num_actions: int = 1


CR = CardReference
type CardList = List[EventCard]


type OptionsFn = Callable[[Any], MoveOptionSet | MoveOptionTree]
type ExecuteFn = Callable[[WotrGame, Any]]


@dataclass
class ActionOperator:
    define_options: OptionsFn
    execute_action: ExecuteFn
