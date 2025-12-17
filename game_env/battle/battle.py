from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_env.army import Army
    from game_env.event_cards.cards import EventCard
    from game_env.game_env_enums import P
    from game_env.regions_enum import R


class Battle:
    region: R
    shadow_army : Army
    free_army : Army
    attacker : P
    shadow_card : EventCard
    free_card : EventCard
