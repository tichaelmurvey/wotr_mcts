"""
Move types
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Tuple

from game_env.characters import CompanionName
from game_env.event_cards.cards import DeckType, EventCard
from game_env.game_env_enums import Player
from game_env.regions_enum import R


class OptsPolicy(IntEnum):
    FLAT = 0
    TREE = 1


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

    #Dice resolutions
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
    
    #special dice actions
    CONVERT_TO_EYE=25
    CONVERT_TO_WOTW=26
    KILL_WOTW=27
    USE_RING_FP=28
    USE_RING_SP=29


MT = MoveType


@dataclass
class CardReference:
    player: Player
    deck: DeckType
    idx: int

type MoveTarget = None | CardReference | R | CompanionName | int


@dataclass
class MoveOption:
    move_type: MoveType
    move_target: MoveTarget


MO = MoveOption


@dataclass
class MoveOptionSet:
    options: Tuple[MoveOption, ...]
    num: int = 1
    policy: OptsPolicy = OptsPolicy.FLAT


MOS = MoveOptionSet

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



