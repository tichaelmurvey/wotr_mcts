from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from game_env.moves.move_types import (
        CR,
        MO,
        MT,
        CardList,
        CardReference,
        MoveOptionSet,
    )

from game_env.event_cards.cards import HAND_LIMIT
from game_env.moves.action_generator import ActionOperator


def _define_options(hand: CardList):
    overage = len(hand) - HAND_LIMIT
    if overage <= 0:
        raise Exception("Invalid discard move!")

    discard_options = tuple(
        MO(MT.EVENT_CARD_DISCARD, CR(card.player, card.deck_type, card.idx))
        for card in hand
    )

    return MoveOptionSet(discard_options, overage)


def _execute_action(game_env: WotrGame, move_target: CardReference):
    game_env.player_states[move_target.player].card_manager.discard_card(move_target)


discard_operator = ActionOperator(_define_options, _execute_action)
