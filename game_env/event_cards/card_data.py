from __future__ import annotations
from typing import TYPE_CHECKING, List

from game_env.event_cards.combat_effects import mumakil, swarm_of_bats
from game_env.action_signal_types import ActionSignal
from game_env.army import SU, UnitGroupShadow
from game_env.characters import M
from game_env.event_cards.cards import (
    CA,
    CB,
    EventCard,
)
from game_env.event_cards.condition_checkers import character_in_play
from game_env.game_env_enums import P
from game_env.moves.move_types import MT
from game_env.regions_enum import R

FREE_CHARACTER : List[EventCard] = []
FREE_STRATEGY: List[EventCard] = []
SHADOW_CHARACTER : List[EventCard]= []
SHADOW_STRATEGY: List[EventCard] = []

if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from game_env.battle.battle import Battle


def wk_returns_effect(game_env: WotrGame):
    game_env.minion_pos[M.WITCH_KING] = R.ANGMAR
    game_env.recruit(
        R.ANGMAR, UnitGroupShadow({SU.mord_reg: 2, SU.mord_elt: 1}), P.SHADOW
    )

def shadows_gather_effect(game_env: WotrGame):
    game_env.action_triage.append(ActionSignal(MT.SHADOWS_GATHER))


def to_do(battle : Battle):
    pass

witch_king_returns = EventCard(
    action_type=CA.STRATEGY_MUSTER,
    deck_type=CB.STRATEGY,
    player=P.SHADOW,
    idx=12,
    title="Return of the Witch-king",
    condition_text="Play if the Witch-king is in play.",
    description="Move the Witch-king to Angmar, then recruit two Sauron Regular units and one Sauron Elite unit there.",
    effect_method=wk_returns_effect,
    condition_checker=character_in_play(M.WITCH_KING),
    combat_effect=swarm_of_bats,
)

shadows_gather = EventCard(
    action_type=CA.STRATEGY_ARMY,
    deck_type=CB.STRATEGY,
    player=P.SHADOW,
    idx=7,
    title="Shadows Gather",
    description="Move one shadow army up to three regions.",
    effect_method=shadows_gather_effect,
    combat_effect=mumakil,
)

SHADOW_STRATEGY.append(witch_king_returns)
SHADOW_STRATEGY.append(shadows_gather)