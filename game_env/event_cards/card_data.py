from __future__ import annotations
from typing import TYPE_CHECKING
from game_env.army import SU, UnitGroupShadow
from game_env.characters import M
from game_env.event_cards.cards import (
    CA,
    CB,
    CombatEffect,
    EventCard,
)
from game_env.game_env_enums import P
from game_env.regions_enum import R

FREE_CHARACTER = []
FREE_STRATEGY = []
SHADOW_CHARACTER = []
SHADOW_STRATEGY = []

if TYPE_CHECKING:
    from game_env.game_env import WotrGame

def wk_angmar(game_env: WotrGame):
    game_env.minion_pos[M.WITCH_KING] = R.ANGMAR
    game_env.recruit(
        R.ANGMAR, UnitGroupShadow({SU.mord_reg: 2, SU.mord_elt: 1}), P.SHADOW
    )


def do_nothing():
    pass


swarm_of_bats = CombatEffect(
    "Swarm of Bats",
    "Cancel the effects of the Combat card played by the Free Peoples player."
    "If the Free Peoples player did not play a card, add 1 to all dice on your Leader re-roll.",
    do_nothing,
    priority=0,
)

example_card = EventCard(
    action_type=CA.STRATEGY_MUSTER,
    deck_type=CB.STRATEGY,
    player=P.SHADOW,
    idx=12,
    title="Return of the Witch-king",
    condition_text="Play if the Witch-king is in play.",
    description="Move the Witch-king to Angmar, then recruit two Sauron Regular units and one Sauron Elite unit there.",
    effect_method=wk_angmar,
    condition_checker=do_nothing,
    combat_effect=swarm_of_bats,
)
