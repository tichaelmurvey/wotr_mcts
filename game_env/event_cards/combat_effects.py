from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_env.battle.battle import Battle

from game_env.army import AU
from game_env.event_cards.cards import CombatEffect
from game_env.event_cards.condition_checkers import units_in_battle
def to_do(battle : Battle):
    pass

swarm_of_bats = CombatEffect(
    title = "Swarm of Bats",
    description = "Cancel the effects of the Combat card played by the Free Peoples player."
    "If the Free Peoples player did not play a card, add 1 to all dice on your Leader re-roll.",
    effect_method = to_do,
    priority=0,
)
mumakil = CombatEffect(
    title="Mumakil",
    description="Add 1 to all dice on your Combat Roll.",
    priority=3,
    effect_method=to_do,
    condition_text="Play if a Southrons and Easterlins Elite unit is in the battle.",
    condition_checker=units_in_battle((AU.east_reg, AU.east_elt))
)