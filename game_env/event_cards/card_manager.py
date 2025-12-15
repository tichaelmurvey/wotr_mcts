from __future__ import annotations
import random
from typing import TYPE_CHECKING, List, NamedTuple
if TYPE_CHECKING:
    from game_env.action_signal_types import ActionRequirement
    from game_env.moves.move_types import CardReference
    from game_env.event_cards.cards import EventCard
from game_env.action_signal_types import S
from game_env.game_env_enums import P
from game_env.moves.action_generator import MT

from game_env.event_cards.cards import HAND_LIMIT, DeckType

class Deck:
    def __init__(self, cards: List[EventCard]):
        self.cards = cards
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            print("returning none")
            return None
        return self.cards.pop()


class PlayerDecks(NamedTuple):
    character: Deck
    strategy: Deck


class EventCardManager:
    hand: List[EventCard]
    discard_pile: List[EventCard]
    decks: PlayerDecks

    def __init__(
        self, action_requirement: ActionRequirement, player: P, decks: PlayerDecks
    ):
        self.player = player
        self.action_requirement = action_requirement
        self.decks = decks
        self.hand = []

    def draw_card(self, deck_type: DeckType):
        card = self.decks[deck_type].draw_card()
        print("drew card", card)
        if card != None:
            self.hand.append(card)

    def draw_cards_move(self, n_char=0, n_strat=0):
        for _ in range(n_char):
            self.draw_card(DeckType.CHARACTER)

        for _ in range(n_strat):
            self.draw_card(DeckType.CHARACTER)

        if len(self.hand) > HAND_LIMIT:
            self.action_requirement.append(S(MT.EVENT_CARD_DISCARD, self.player))

    def discard_card(self, card_ref: CardReference):
        for i, x in enumerate(self.hand):
            if (x.deck_type == card_ref.deck) and (x.idx == card_ref.idx):
                self.discard_pile.append(self.hand.pop(i))
                break
