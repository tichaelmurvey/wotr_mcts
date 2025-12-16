"""
Input handling for War of the Ring interface.

Processes mouse and keyboard events and dispatches them to appropriate components.
"""

from typing import TYPE_CHECKING, Optional, Tuple
import pygame

from pygame_interface.config import InteractionState

if TYPE_CHECKING:
    from pygame_interface.game_interface import WotrInterface


class InputHandler:
    """
    Handles all user input for the interface.

    Processes pygame events and dispatches actions to the appropriate
    components based on the current interaction state.
    """

    def __init__(self, interface: "WotrInterface"):
        """
        Initialize the input handler.

        Args:
            interface: The main WotrInterface instance
        """
        self.interface = interface

        # Drag state for board panning
        self.dragging = False
        self.drag_start: Optional[Tuple[int, int]] = None

        # Last mouse position for hover effects
        self.last_mouse_pos: Tuple[int, int] = (0, 0)

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a pygame event.

        Args:
            event: The pygame event to process
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_up(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
        elif event.type == pygame.MOUSEWHEEL:
            self._handle_mouse_wheel(event)
        elif event.type == pygame.KEYDOWN:
            self._handle_key_down(event)
        elif event.type == pygame.KEYUP:
            self._handle_key_up(event)

    def _handle_mouse_down(self, event: pygame.event.Event):
        """Handle mouse button press."""
        pos = event.pos

        # Right click - start panning
        if event.button == 3:  # Right mouse button
            if self.interface.board.rect.collidepoint(pos):
                self.dragging = True
                self.drag_start = pos
                self.interface.board.start_pan(pos)
            return

        # Left click
        if event.button == 1:
            self._handle_left_click(pos)

    def _handle_left_click(self, pos: Tuple[int, int]):
        """Handle left mouse button click."""
        interface = self.interface

        # Check if card panel is showing expanded card
        if interface.card_panel.expanded_card:
            interface.card_panel.close_expanded()
            return

        # Check action panel buttons
        if interface.action_panel.rect.collidepoint(pos):
            if interface.action_panel.handle_click(pos):
                return

        # Check card panel
        if interface.card_panel.rect.collidepoint(pos):
            card = interface.card_panel.handle_click(pos)
            if card:
                self._handle_card_selection(card)
            return

        # Check sidebar (scroll handling, etc.)
        if interface.sidebar.rect.collidepoint(pos):
            # Sidebar doesn't have clickable elements for now
            return

        # Check board
        if interface.board.rect.collidepoint(pos):
            self._handle_board_click(pos)

    def _handle_board_click(self, pos: Tuple[int, int]):
        """Handle a click on the game board."""
        interface = self.interface
        region = interface.get_region_at_pos(pos)

        if region is None:
            # Clicked empty area - cancel selection
            if interface.selected_region is not None:
                interface.cancel_selection()
            return

        state = interface.interaction_state

        if state == InteractionState.IDLE:
            # No active selection needed
            pass

        elif state == InteractionState.SELECTING_SOURCE:
            # Select source region
            self._select_source_region(region)

        elif state == InteractionState.SELECTING_DESTINATION:
            # Select destination region
            self._select_destination_region(region)

    def _select_source_region(self, region):
        """Handle selection of a source region."""
        interface = self.interface

        # Check if region is valid source
        if interface.move_builder.is_valid_source(region):
            interface.selected_region = region
            interface.board.set_selected_region(region)

            # Get valid destinations
            destinations = interface.move_builder.get_valid_destinations(region)
            if destinations:
                interface.set_valid_destinations(destinations)
                interface.interaction_state = InteractionState.SELECTING_DESTINATION
                interface.action_panel.set_message(f"Select destination from {region.name}")
            else:
                # No valid destinations - might be other action type
                interface.move_builder.handle_source_selection(region)

    def _select_destination_region(self, region):
        """Handle selection of a destination region."""
        interface = self.interface

        if region in interface.valid_destinations:
            # Valid destination - complete the move
            interface.move_builder.handle_destination_selection(region)
            interface.clear_highlights()
            interface.selected_region = None
            interface.interaction_state = InteractionState.SELECTING_SOURCE
        elif region == interface.selected_region:
            # Clicked same region - cancel
            interface.cancel_selection()
        else:
            # Invalid destination - show message
            interface.show_message("Invalid destination", 1.5)

    def _handle_card_selection(self, card):
        """Handle selection of a card."""
        interface = self.interface

        # Notify move builder about card selection
        interface.move_builder.handle_card_selection(card)

    def _handle_mouse_up(self, event: pygame.event.Event):
        """Handle mouse button release."""
        if event.button == 3:  # Right mouse button
            if self.dragging:
                self.dragging = False
                self.interface.board.end_pan()

    def _handle_mouse_motion(self, event: pygame.event.Event):
        """Handle mouse movement."""
        pos = event.pos
        self.last_mouse_pos = pos

        # Update panning if dragging
        if self.dragging:
            self.interface.board.update_pan(pos)
            return

        # Update hover states
        self._update_hover_states(pos)

    def _update_hover_states(self, pos: Tuple[int, int]):
        """Update hover states for all components."""
        interface = self.interface

        # Board hover - region detection
        if interface.board.rect.collidepoint(pos):
            region = interface.get_region_at_pos(pos)
            interface.board.set_hovered_region(region)
            interface.hovered_region = region
        else:
            interface.board.set_hovered_region(None)
            interface.hovered_region = None

        # Card panel hover
        interface.card_panel.handle_mouse_motion(pos)

        # Action panel hover
        interface.action_panel.handle_mouse_motion(pos)

    def _handle_mouse_wheel(self, event: pygame.event.Event):
        """Handle mouse wheel scrolling."""
        pos = self.last_mouse_pos

        # Zoom board if mouse is over it
        if self.interface.board.rect.collidepoint(pos):
            zoom_factor = 1.1 if event.y > 0 else 0.9
            new_zoom = self.interface.board.zoom * zoom_factor
            self.interface.board.set_zoom(new_zoom, pos)
            return

        # Scroll card panel
        if self.interface.card_panel.rect.collidepoint(pos):
            self.interface.card_panel.handle_scroll(-event.y)
            return

        # Scroll sidebar
        if self.interface.sidebar.rect.collidepoint(pos):
            self.interface.sidebar.handle_scroll(-event.y)

    def _handle_key_down(self, event: pygame.event.Event):
        """Handle key press."""
        key = event.key

        # Escape - cancel current action
        if key == pygame.K_ESCAPE:
            self._handle_escape()
            return

        # Space - confirm/pass
        if key == pygame.K_SPACE:
            self._handle_space()
            return

        # Tab - switch card panel view
        if key == pygame.K_TAB:
            self._toggle_card_panel_player()
            return

        # Number keys - quick action selection
        if pygame.K_1 <= key <= pygame.K_9:
            idx = key - pygame.K_1
            self._select_quick_action(idx)
            return

        # R - reset board view
        if key == pygame.K_r:
            self.interface.board._fit_board_to_rect()
            return

    def _handle_key_up(self, event: pygame.event.Event):
        """Handle key release."""
        pass

    def _handle_escape(self):
        """Handle escape key press."""
        interface = self.interface

        # Close expanded card
        if interface.card_panel.expanded_card:
            interface.card_panel.close_expanded()
            return

        # Close dialog
        if interface.dialog_manager.is_open():
            interface.dialog_manager.close()
            return

        # Cancel current selection
        interface.cancel_selection()

    def _handle_space(self):
        """Handle space key press."""
        interface = self.interface

        # If pass is available, trigger it
        if interface.action_panel.buttons[1].enabled:  # Pass button
            interface.action_panel._on_pass_click()

    def _toggle_card_panel_player(self):
        """Toggle which player's cards are shown."""
        from game_env.game_env_enums import Player

        current = self.interface.card_panel.active_player
        new_player = Player.SHADOW if current == Player.FREE else Player.FREE
        self.interface.card_panel.set_active_player(new_player)

    def _select_quick_action(self, index: int):
        """Select an action by number key."""
        interface = self.interface

        if not interface.current_action_space:
            return

        actions = interface.current_action_space.action_set
        if index < len(actions):
            interface.move_builder.select_action_by_index(index)
