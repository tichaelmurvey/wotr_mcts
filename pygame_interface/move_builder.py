"""
Move builder for War of the Ring interface.

Constructs ActionChoice tuples from user interactions.
"""

from typing import TYPE_CHECKING, List, Optional, Set

from game_env.moves.move_types import MoveOption, MoveType
from game_env.regions_enum import R

if TYPE_CHECKING:
    from game_env.moves.move_types import ActionChoice, ActionSpace
    from game_env.event_cards.cards import EventCard
    from pygame_interface.game_interface import WotrInterface


class MoveBuilder:
    """
    Builds ActionChoice tuples from user interactions.

    Tracks the current move being constructed and validates
    selections against the available ActionSpace.
    """

    def __init__(self, interface: "WotrInterface"):
        """
        Initialize the move builder.

        Args:
            interface: The main WotrInterface instance
        """
        self.interface = interface

        # Current action space
        self.action_space: Optional["ActionSpace"] = None

        # Move construction state
        self.selected_source: Optional[R] = None
        self.selected_destination: Optional[R] = None
        self.selected_card: Optional["EventCard"] = None
        self.selected_action_index: Optional[int] = None

        # Cached valid moves
        self._valid_sources: Set[R] = set()
        self._valid_destinations_by_source: dict[R, Set[R]] = {}
        self._region_moves: dict[R, List["ActionChoice"]] = {}

    def set_action_space(self, action_space: "ActionSpace"):
        """
        Set the current action space.

        Args:
            action_space: The available actions from the game engine
        """
        self.action_space = action_space
        self._analyze_action_space()
        self._update_interface_state()

    def reset(self):
        """Reset the move builder state."""
        self.selected_source = None
        self.selected_destination = None
        self.selected_card = None
        self.selected_action_index = None
        self._valid_sources.clear()
        self._valid_destinations_by_source.clear()
        self._region_moves.clear()

    def _analyze_action_space(self):
        """Analyze the action space to extract valid moves."""
        if not self.action_space:
            return

        self._valid_sources.clear()
        self._valid_destinations_by_source.clear()
        self._region_moves.clear()

        for action_choice in self.action_space.action_set:
            if not action_choice:
                continue

            for move in action_choice:
                target = move.move_target

                # Check if target is a region
                if isinstance(target, R):
                    # This could be source or destination depending on move type
                    move_type = move.move_type

                    # For now, treat all region targets as potential destinations
                    # The actual logic depends on move type
                    self._valid_sources.add(target)

                    if target not in self._region_moves:
                        self._region_moves[target] = []
                    self._region_moves[target].append(action_choice)

    def _update_interface_state(self):
        """Update interface to reflect available actions."""
        if not self.action_space:
            self.interface.action_panel.set_message("No actions available")
            return

        # Count action types
        move_types = set()
        for action_choice in self.action_space.action_set:
            if action_choice:
                for move in action_choice:
                    move_types.add(move.move_type)

        # Set message based on available actions
        if MoveType.DECLARE_FELLOWSHIP in move_types:
            self.interface.action_panel.set_message("Declare fellowship or select action")
        elif MoveType.CHANGE_GUIDE in move_types:
            self.interface.action_panel.set_message("Select new guide")
        elif MoveType.EVENT_CARD_DISCARD in move_types:
            self.interface.action_panel.set_message("Select cards to discard")
        elif MoveType.RESOLVE_ACTION_DIE in move_types:
            self.interface.action_panel.set_message("Select action die to use")
        else:
            self.interface.action_panel.set_message(
                f"{len(self.action_space.action_set)} actions available"
            )

        self.interface.action_panel.set_action_space(self.action_space)

    def is_valid_source(self, region: R) -> bool:
        """
        Check if a region is a valid source for the current action.

        Args:
            region: The region to check

        Returns:
            True if the region is a valid source
        """
        return region in self._valid_sources

    def get_valid_destinations(self, source: R) -> Set[R]:
        """
        Get valid destinations from a source region.

        Args:
            source: The source region

        Returns:
            Set of valid destination regions
        """
        # For army movement, destinations are adjacent regions
        # This is a simplified version - actual logic depends on move type
        if source in self._valid_destinations_by_source:
            return self._valid_destinations_by_source[source]

        # Check action space for moves involving this source
        destinations = set()

        if self.action_space:
            for action_choice in self.action_space.action_set:
                if not action_choice:
                    continue

                # Look for move sequences that start with source
                # and have a destination
                for move in action_choice:
                    if isinstance(move.move_target, R):
                        if move.move_target != source:
                            destinations.add(move.move_target)

        self._valid_destinations_by_source[source] = destinations
        return destinations

    def handle_source_selection(self, region: R):
        """
        Handle selection of a source region.

        Args:
            region: The selected source region
        """
        self.selected_source = region

        # Check if this region has direct actions (not requiring destination)
        if region in self._region_moves:
            moves = self._region_moves[region]

            # If only one move, auto-complete it
            if len(moves) == 1:
                self._complete_move(moves[0])
                return

            # Otherwise, show options (could use dialog)
            self.interface.show_message(f"{len(moves)} actions available here", 2.0)

    def handle_destination_selection(self, region: R):
        """
        Handle selection of a destination region.

        Args:
            region: The selected destination region
        """
        self.selected_destination = region

        # Find the matching action choice
        if self.action_space:
            for action_choice in self.action_space.action_set:
                if self._matches_source_destination(
                    action_choice,
                    self.selected_source,
                    region,
                ):
                    self._complete_move(action_choice)
                    return

        # No matching move found
        self.interface.show_message("Invalid move", 1.5)

    def _matches_source_destination(
        self,
        action_choice: "ActionChoice",
        source: Optional[R],
        destination: R,
    ) -> bool:
        """Check if an action choice matches the source/destination."""
        if not action_choice:
            return False

        has_source = source is None
        has_destination = False

        for move in action_choice:
            if isinstance(move.move_target, R):
                if source and move.move_target == source:
                    has_source = True
                if move.move_target == destination:
                    has_destination = True

        return has_source and has_destination

    def handle_card_selection(self, card: "EventCard"):
        """
        Handle selection of a card.

        Args:
            card: The selected event card
        """
        self.selected_card = card

        # Check if this completes a card-based action
        if self.action_space:
            for action_choice in self.action_space.action_set:
                if self._matches_card(action_choice, card):
                    self._complete_move(action_choice)
                    return

    def _matches_card(
        self,
        action_choice: "ActionChoice",
        card: "EventCard",
    ) -> bool:
        """Check if an action choice matches a card selection."""
        if not action_choice:
            return False

        for move in action_choice:
            # Check if move target is a card reference matching this card
            target = move.move_target
            if hasattr(target, "idx") and target.idx == card.idx: # type: ignore
                return True

        return False

    def select_action_by_index(self, index: int):
        """
        Select an action directly by index.

        Args:
            index: Index into the action set
        """
        if not self.action_space:
            return

        actions = self.action_space.action_set
        if index < len(actions):
            self._complete_move(actions[index])

    def _complete_move(self, action_choice: "ActionChoice"):
        """
        Complete the move and submit it to the interface.

        Args:
            action_choice: The completed action choice
        """
        self.interface.submit_move(action_choice)
        self.reset()

    def get_current_state_description(self) -> str:
        """Get a description of the current move builder state."""
        if self.selected_source and not self.selected_destination:
            return f"Moving from {self.selected_source.name}..."
        elif self.selected_card:
            return f"Selected: {self.selected_card.title}"
        elif self.action_space:
            return f"{len(self.action_space.action_set)} actions available"
        else:
            return "Waiting for move..."
