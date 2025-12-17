from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Callable, NamedTuple

if TYPE_CHECKING:
    from game_env.battle.battle import Battle
    from game_env.game_env import WotrGame
    from game_env.game_env_enums import TABLE_CARD_TRIGGER, Player
HAND_LIMIT = 6


class CardActionType(IntEnum):
    CHARACTER = 0
    STRATEGY_ARMY = 1
    STRATEGY_MUSTER = 2


CA = CardActionType


class DeckType(IntEnum):
    CHARACTER = 0
    STRATEGY = 1


CB = DeckType


class CombatEffect(NamedTuple):
    title: str
    description: str
    effect_method: Callable[[Battle]]
    priority: int
    condition_text: str | None = None
    condition_checker: Callable[[Battle], bool] | None = None

CE = CombatEffect


@dataclass
class EventCard:
    action_type: CardActionType
    deck_type: DeckType
    player: Player
    idx: int
    title: str
    description: str
    effect_method: Callable
    combat_effect: CombatEffect
    table_trigger: TABLE_CARD_TRIGGER | None = None
    condition_text: str | None = None
    condition_checker: Callable[[WotrGame], bool] | None = None


EC = EventCard
