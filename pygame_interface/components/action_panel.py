"""
Action panel component for War of the Ring interface.

Displays available actions and provides buttons for player interaction.
"""

from typing import TYPE_CHECKING, Callable, List, Optional, Tuple
import pygame

from pygame_interface.config import (
    Colors,
    BUTTON_HEIGHT,
    BUTTON_MIN_WIDTH,
    BUTTON_PADDING,
    FONT_SIZE_MEDIUM,
    FONT_SIZE_SMALL,
)
from pygame_interface.assets import get_asset_manager

if TYPE_CHECKING:
    from game_env.moves.move_types import ActionSpace, MoveOption


class Button:
    """Simple button widget."""

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        callback: Optional[Callable] = None,
        enabled: bool = True,
        color: Tuple[int, int, int] = Colors.PANEL_BORDER,
    ):
        self.rect = rect
        self.text = text
        self.callback = callback
        self.enabled = enabled
        self.color = color
        self.hovered = False

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw the button."""
        # Determine colors
        if not self.enabled:
            bg_color = Colors.DARK_GRAY
            text_color = Colors.TEXT_MUTED
        elif self.hovered:
            bg_color = tuple(min(c + 30, 255) for c in self.color)
            text_color = Colors.TEXT_PRIMARY
        else:
            bg_color = self.color
            text_color = Colors.TEXT_PRIMARY

        # Draw background
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, self.rect, 1)

        # Draw text
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle click, return True if button was clicked."""
        if self.enabled and self.rect.collidepoint(pos):
            if self.callback:
                self.callback()
            return True
        return False

    def handle_motion(self, pos: Tuple[int, int]):
        """Handle mouse motion for hover state."""
        self.hovered = self.rect.collidepoint(pos)


class ActionPanel:
    """
    Panel for displaying available actions and action buttons.
    """

    def __init__(self, rect: pygame.Rect):
        """
        Initialize the action panel.

        Args:
            rect: The rectangle area for the panel
        """
        self.rect = rect
        self.assets = get_asset_manager()

        # Current action space
        self.action_space: Optional["ActionSpace"] = None
        self.available_moves: List[str] = []

        # Message to display
        self.message: str = "Waiting for game..."

        # Buttons
        self.buttons: List[Button] = []

        # Callbacks
        self.on_pass: Optional[Callable] = None
        self.on_cancel: Optional[Callable] = None
        self.on_end_turn: Optional[Callable] = None

        self._create_default_buttons()

    def set_rect(self, rect: pygame.Rect):
        """Update the display rectangle."""
        self.rect = rect
        self._reposition_buttons()

    def _create_default_buttons(self):
        """Create the default action buttons."""
        self.buttons = [
            Button(
                pygame.Rect(0, 0, BUTTON_MIN_WIDTH, BUTTON_HEIGHT),
                "Cancel",
                self._on_cancel_click,
                enabled=False,
            ),
            Button(
                pygame.Rect(0, 0, BUTTON_MIN_WIDTH, BUTTON_HEIGHT),
                "Pass",
                self._on_pass_click,
                enabled=False,
            ),
            Button(
                pygame.Rect(0, 0, BUTTON_MIN_WIDTH + 20, BUTTON_HEIGHT),
                "End Turn",
                self._on_end_turn_click,
                enabled=False,
            ),
        ]
        self._reposition_buttons()

    def _reposition_buttons(self):
        """Reposition buttons based on current rect."""
        if not self.buttons:
            return

        # Position buttons on the right side
        x = self.rect.right - BUTTON_PADDING
        y = self.rect.y + (self.rect.height - BUTTON_HEIGHT) // 2

        for button in reversed(self.buttons):
            button.rect.right = x
            button.rect.y = y
            x -= button.rect.width + BUTTON_PADDING

    def _on_cancel_click(self):
        """Handle cancel button click."""
        if self.on_cancel:
            self.on_cancel()

    def _on_pass_click(self):
        """Handle pass button click."""
        if self.on_pass:
            self.on_pass()

    def _on_end_turn_click(self):
        """Handle end turn button click."""
        if self.on_end_turn:
            self.on_end_turn()

    def set_action_space(self, action_space: Optional["ActionSpace"]):
        """
        Set the current available actions.

        Args:
            action_space: The ActionSpace from the game engine
        """
        self.action_space = action_space

        if action_space:
            # Extract move descriptions
            self.available_moves = []
            for action_choice in action_space.action_set[:5]:  # Limit display
                if action_choice:
                    move = action_choice[0]  # First move in choice
                    self.available_moves.append(move.move_type.name)

            # Enable cancel button
            self.buttons[0].enabled = True
        else:
            self.available_moves = []
            self.buttons[0].enabled = False

    def set_message(self, message: str):
        """Set the message to display."""
        self.message = message

    def enable_pass(self, enabled: bool = True):
        """Enable or disable the pass button."""
        self.buttons[1].enabled = enabled

    def enable_end_turn(self, enabled: bool = True):
        """Enable or disable the end turn button."""
        self.buttons[2].enabled = enabled

    def enable_cancel(self, enabled: bool = True):
        """Enable or disable the cancel button."""
        self.buttons[0].enabled = enabled

    def update(self):
        """Update panel state."""
        pass

    def draw(self, screen: pygame.Surface):
        """Draw the action panel."""
        # Draw background
        pygame.draw.rect(screen, Colors.PANEL_BG, self.rect)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, self.rect, 2)

        font_medium = self.assets.get_font(FONT_SIZE_MEDIUM)
        font_small = self.assets.get_font(FONT_SIZE_SMALL)

        # Draw message
        message_text = font_medium.render(self.message, True, Colors.TEXT_PRIMARY)
        screen.blit(
            message_text,
            (self.rect.x + BUTTON_PADDING, self.rect.y + 10),
        )

        # Draw available moves summary
        if self.available_moves:
            moves_text = ", ".join(self.available_moves[:3])
            if len(self.available_moves) > 3:
                moves_text += f" (+{len(self.available_moves) - 3} more)"
            moves_surface = font_small.render(
                f"Available: {moves_text}",
                True,
                Colors.TEXT_SECONDARY,
            )
            screen.blit(
                moves_surface,
                (self.rect.x + BUTTON_PADDING, self.rect.y + 35),
            )

        # Draw buttons
        for button in self.buttons:
            button.draw(screen, font_small)

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """
        Handle a click on the panel.

        Args:
            pos: (x, y) screen position

        Returns:
            True if a button was clicked
        """
        for button in self.buttons:
            if button.handle_click(pos):
                return True
        return False

    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """Handle mouse motion for hover effects."""
        for button in self.buttons:
            button.handle_motion(pos)
