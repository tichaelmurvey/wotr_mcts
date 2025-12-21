from __future__ import annotations
from copy import deepcopy
from typing import TYPE_CHECKING, List, Tuple, cast

from game_env.army import GenericUnitGroup
from game_env.moves.ACTION_OPTION_OBSERVERS import ACTION_OPTION_OBSERVERS
from game_env.moves.ACTION_RESOLVERS import ACTION_RESOLVERS
from game_env.politics.politics import Politics

if TYPE_CHECKING:
    from game_env.action_signal_types import ActionRequirement
    from game_env.army import UnitGroup, UnitGroupShadow
    from game_env.action_signal_types import S
    from game_env.regions.region import R, Region

from game_env.characters import C, M
from game_env.action_dice.dice import ActionDieFree, ActionDieShadow, ActionResult
from game_env.action_dice.dice_pool import DicePool
from game_env.event_cards.card_data import (
    FREE_CHARACTER,
    FREE_STRATEGY,
    SHADOW_CHARACTER,
    SHADOW_STRATEGY,
)
from game_env.event_cards.card_manager import (
    Deck,
    EventCardManager,
    PlayerDecks,
)
from game_env.event_cards.cards import EC
from game_env.fellowship import Fellowship
from game_env.game_env_enums import (
    GAME_PHASE,
    GP,
    P,
    TABLE_CARD_TRIGGER,
    Player,
)
from game_env.hunt.hunt import Hunt, HuntBox
from game_env.hunt.hunt_pool import HuntPool
from game_env.moves.move_manager import (
    MoveManager,
)
from game_env.moves.move_types import MT, ActionChoice, ActionSpace, MoveOptionTree
from game_env.regions.regions_data import regions_init
from game_env.regions.starting_positions import STARTING_POSITIONS


class WotrGame:
    current_action_space: ActionSpace | None
    current_action_tree: MoveOptionTree | None
    table_cards: List[EC]
    active_hunt: Hunt | None
    minion_pos: dict[M, R | None]
    companion_pos: dict[C, R | None]
    phase: GAME_PHASE
    turn: int
    regions: Tuple[Region, ...]
    politics: Politics
    active_die_player: P
    converting_die: None | ActionResult
    verbose: bool

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.reset()
        print("instancing")

    def reset(self):
        if self.verbose:
            print("resetting")
        self.regions = deepcopy(regions_init)
        self.politics = Politics()
        self.table_cards = []

        self.action_triage: ActionRequirement = []
        self.move_manager = MoveManager(self)

        self.fellowship = Fellowship(self.action_triage, self.regions)
        self.hunt_pool = HuntPool()
        self.hunt_box = HuntBox()
        self.active_hunt = None

        self.player_state_free = PlayerStateFree(self.action_triage)
        self.player_state_shadow = PlayerStateShadow(self.action_triage)
        self.player_states = (self.player_state_free, self.player_state_shadow)

        self.phase = GP.DRAW_CARDS
        self.turn = 0
        self.active_die_player = P.FREE
        self.converting_die = None

        self.reset_armies()

        self.minion_pos = {M.SARUMAN: None, M.MOUTH: None, M.WITCH_KING: None}

    def start_game(self, verbose: bool = False):
        self.verbose = verbose
        if verbose:
            print("starting game")
        self.reset()
        self.progress_game()

    def reset_armies(self):
        for STARTING_POSITION in STARTING_POSITIONS:
            self.regions[STARTING_POSITION.region_id].set_starting_units(
                STARTING_POSITION.units
            )

    def update_phase(self):
        self.phase = GAME_PHASE(self.phase + 1 if self.phase < 6 else 1)

    def execute_player_action(self, action_choice: ActionChoice):
        # do move(s)
        self.move_manager.execute_player_action(action_choice)

        if self.move_manager.action_tree is not None:
            return

        if len(self.action_triage) == 0:
            self.update_phase()
        self.progress_game()

    def offer_move(self):
        action_needed = self.action_triage.pop()
        self.move_manager.generate_moves(action_needed)

    def progress_game(self):
        if self.verbose:
            print("progressing game")
        if len(self.action_triage) > 0:
            if self.verbose:
                print("action in triage, offering move")
            # resolve an outstanding player action
            self.offer_move()
            return

        else:
            if self.verbose:
                print("checking phase ", self.phase.name)
            match self.phase:
                case GP.DRAW_CARDS:
                    self.draw_cards_phase()

                case GP.FELLOWSHIP:
                    self.fellowship.fellowship_phase()

                case GP.HUNT_ALLOCATION:
                    self.hunt_allocation()

                case GP.ACTION_ROLL:
                    self.action_roll()
                case GP.ACTION_RESOLUTION:
                    self.action_resolution()
                case GP.VICTORY_CHECK:
                    self.victory_check()
            if len(self.action_triage) == 0:
                if self.verbose:
                    self.print_game()
                self.update_phase()

            self.progress_game()

    def draw_cards_phase(self):
        # increment turn
        self.turn += 1
        # recover action dice
        for player in self.player_states:
            player.dice_pool.recover_dice()

        # draw one card from each deck for each player
        for player in self.player_states:
            player.card_manager.draw_cards_move(1, 1)

    def hunt_allocation(self):
        self.action_triage.append(
            S(MT.HUNT_ALLOCATION, move_data=self, action_player=P.SHADOW)
        )

    def action_roll(self):
        for player in self.player_states:
            player.dice_pool.action_roll()

        shadow_pool = self.player_state_shadow.dice_pool.action_dice
        free_pool = self.player_state_free.dice_pool.action_dice
        for i in range(len(shadow_pool) + len(free_pool) - self.hunt_box.eyes):
            self.action_triage.append(S(MT.RESOLVE_ACTION_DIE, move_data=self))

    def action_resolution(self):
        pass

    def victory_check(self):
        pass

    def recruit(self, region_code: R, new_units: GenericUnitGroup, units_player: P):
        region = self.regions[region_code]
        if region.army and region.army.player is not units_player:
            return

        region.units = region.units + new_units

    def check_table_triggers(self, TAG: TABLE_CARD_TRIGGER, move: MT):
        triggered_cards = [
            card for card in self.table_cards if card.table_trigger == TAG
        ]
        if len(triggered_cards) > 0:
            self.action_triage.append(S(move, move_data=triggered_cards))
            return True
        return False

    def print_game(self):
        print("===== GAME STATE =====")
        print(f"Turn {self.turn} phase: {self.phase}")
        self.player_state_shadow.print_game()
        self.player_state_free.print_game()


class PlayerState:
    player: Player
    card_manager: EventCardManager
    dice_pool: DicePool
    elven_rings: int

    def __init__(self, action_requirement: ActionRequirement):
        self.action_requirement = action_requirement

    def print_game(self):
        print(f"Player {self.player} game state")
        print(f"Card hand: ")
        for card in self.card_manager.hand:
            print(card.title)


class PlayerStateShadow(PlayerState):
    def __init__(self, action_requirement: ActionRequirement):
        super().__init__(action_requirement)
        self.player = P.SHADOW
        self.elven_rings = 0
        self.card_manager = EventCardManager(
            action_requirement,
            P.SHADOW,
            PlayerDecks(Deck(SHADOW_CHARACTER), Deck(SHADOW_STRATEGY)),
        )
        self.dice_pool = DicePool(ActionDieShadow, 7)


class PlayerStateFree(PlayerState):
    def __init__(self, action_requirement: ActionRequirement):
        super().__init__(action_requirement)
        self.player = P.FREE
        self.elven_rings = 3
        self.card_manager = EventCardManager(
            action_requirement,
            P.FREE,
            PlayerDecks(Deck(FREE_CHARACTER), Deck(FREE_STRATEGY)),
        )
        self.dice_pool = DicePool(ActionDieFree, 4)


def get_opposite_player(player: P):
    return P.FREE if player is P.SHADOW else P.SHADOW
