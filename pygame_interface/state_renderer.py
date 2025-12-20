"""
State renderer for War of the Ring interface.

Reads game state from WotrGame and updates UI components accordingly.
"""

from typing import TYPE_CHECKING, Optional
from collections import Counter

from game_env.action_dice.dice_pool import DicePool
from game_env.game_env_enums import Player
from game_env.regions_enum import R

if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from pygame_interface.game_interface import WotrInterface


class StateRenderer:
    """
    Reads game state and updates UI components.

    This class serves as the bridge between the game engine's state
    and the visual representation in the interface.
    """

    def __init__(self, interface: "WotrInterface"):
        """
        Initialize the state renderer.

        Args:
            interface: The main WotrInterface instance
        """
        self.interface = interface

        # Cached state
        self.current_player: Optional[Player] = None
        self.current_phase: Optional[str] = None
        self.current_turn: int = 0

    def update_from_game(self, game: "WotrGame"):
        """
        Update all UI components from game state.

        Args:
            game: The WotrGame instance to read state from
        """
        if self.interface.debug:
            print("update_from_game")
        if self.interface.debug:
            print("update_regions")
        self._update_regions(game)
        self._update_fellowship(game)
        self._update_player_state(game)
        self._update_cards(game)
        self._update_dice(game)
        if self.interface.debug:
            print("update_phase_info")
        self._update_phase_info(game)
        if self.interface.debug:
            print("end of update_from_game")

    def _update_regions(self, game: "WotrGame"):
        """Update region unit data from game state."""
        board = self.interface.board

        # Clear existing unit data
        board.region_units.clear()
        board.region_characters.clear()
        board.region_control.clear()

        # Iterate through all regions
        for region in game.regions:
            r_enum = R(region.idx)

            # Update units
            if region.units:
                board.set_region_units(r_enum, region.units)

            # Update characters
            characters = []
            if region.wild_companions:
                for companion in region.wild_companions:
                    characters.append(companion.name.lower())
            if region.wild_minions:
                for minion in region.wild_minions:
                    characters.append(minion.name.lower())
            if characters:
                board.set_region_characters(r_enum, characters)

            # Update control
            if region.control is not None:
                board.set_region_control(r_enum, region.control)

    def _update_fellowship(self, game: "WotrGame"):
        """Update fellowship display from game state."""
        fellowship = game.fellowship

        if fellowship and fellowship.region:
            self.interface.board.set_fellowship(
                R(fellowship.region.idx),
                fellowship.revealed,
            )
        else:
            self.interface.board.set_fellowship(None)

        # Update fellowship info in sidebar
        if fellowship:
            self.interface.sidebar.set_fellowship_info(
                position=fellowship.track_position,
                corruption=fellowship.corruption,
                guide=fellowship.guide.name if fellowship.guide else None,
                companions=[c.name for c in fellowship.companions],
                revealed=fellowship.revealed,
                in_mordor=fellowship.in_mordor,
            )

            # Update fellowship box display on the board
            # Companions list excludes the guide
            companions_without_guide = [
                c for c in fellowship.companions if c != fellowship.guide
            ]
            self.interface.board.set_fellowship_box_data(
                companions=companions_without_guide,
                guide=fellowship.guide,
            )

    def _update_player_state(self, game: "WotrGame"):
        """Update player-specific state."""
        # Update Free Peoples state
        fp_state = game.player_state_free
        self.interface.sidebar.set_free_peoples_info(
            cards_in_hand=len(fp_state.card_manager.hand),
            dice_available=self._count_available_dice(fp_state.dice_pool),
        )

        # Update Shadow state
        shadow_state = game.player_state_shadow
        self.interface.sidebar.set_shadow_info(
            cards_in_hand=len(shadow_state.card_manager.hand),
            dice_available=self._count_available_dice(shadow_state.dice_pool),
        )

        # Update reinforcement pools
        self._update_reinforcement_pools(game)

    def _count_available_dice(self, dice_pool: DicePool) -> int:
        """Count dice that haven't been used this turn."""
        return sum(1 for die in dice_pool.action_dice if not die.action_used)

    def _update_reinforcement_pools(self, game: "WotrGame"):
        """Update the reinforcement pool displays."""
        # This would calculate remaining units not on the board
        # For now, we'll set placeholder data
        # In a full implementation, you'd track total units per nation
        # and subtract those currently on the board
        pass

    def _update_cards(self, game: "WotrGame"):
        """Update card displays from game state."""
        # Update Free Peoples hand
        fp_hand = game.player_state_free.card_manager.hand
        self.interface.card_panel.set_hand(Player.FREE, fp_hand)

        # Update Shadow hand
        shadow_hand = game.player_state_shadow.card_manager.hand
        self.interface.card_panel.set_hand(Player.SHADOW, shadow_hand)

        # Update table cards
        self.interface.sidebar.set_table_cards(game.table_cards)

    def _update_dice(self, game: "WotrGame"):
        """Update dice displays from game state."""
        # Free Peoples dice
        fp_dice = game.player_state_free.dice_pool.action_dice
        fp_results = [(die.current_result, die.action_used) for die in fp_dice]
        self.interface.sidebar.set_free_dice(fp_results)

        # Shadow dice
        shadow_dice = game.player_state_shadow.dice_pool.action_dice
        shadow_results = [(die.current_result, die.action_used) for die in shadow_dice]
        self.interface.sidebar.set_shadow_dice(shadow_results)

        # Hunt box
        self.interface.sidebar.set_hunt_box(
            fp_dice=game.hunt_box.fp_dice,
            eyes=game.hunt_box.eyes,
        )

    def _update_phase_info(self, game: "WotrGame"):
        """Update phase and turn display."""
        self.current_turn = game.turn
        self.current_phase = game.phase.name if game.phase else "Unknown"

        self.interface.sidebar.set_phase_info(
            turn=game.turn,
            phase=self.current_phase,
        )

    def get_units_in_region(self, game: "WotrGame", region: R) -> Counter:
        """
        Get the units in a specific region.

        Args:
            game: The WotrGame instance
            region: The R enum value

        Returns:
            Counter of units in the region
        """
        region_obj = game.regions[region]
        return region_obj.units if region_obj.units else Counter()

    def get_region_owner(self, game: "WotrGame", region: R) -> Optional[Player]:
        """
        Get the player who controls a region.

        Args:
            game: The WotrGame instance
            region: The R enum value

        Returns:
            Player enum value or None
        """
        region_obj = game.regions[region]
        if region_obj.army:
            return region_obj.army.player
        return region_obj.control
