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
    from game_env.moves.move_types import ActionChoice, ActionSpace, MoveOption


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

        # Default control buttons (Cancel, Pass, End Turn)
        self.buttons: List[Button] = []

        # Move option buttons (dynamically created)
        self.move_buttons: List[Button] = []

        # Scroll offset for move buttons (when there are many)
        self.scroll_offset: int = 0
        self.max_visible_buttons: int = 8

        # Callbacks
        self.on_pass: Optional[Callable] = None
        self.on_cancel: Optional[Callable] = None
        self.on_end_turn: Optional[Callable] = None
        self.on_move_selected: Optional[Callable[["ActionChoice"], None]] = None

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
        self.scroll_offset = 0

        if action_space:
            # Extract move descriptions
            self.available_moves = []
            for action_choice in action_space.action_set[:5]:  # Limit display
                if action_choice:
                    move = action_choice[0]  # First move in choice
                    self.available_moves.append(move.move_type.name)

            # Enable cancel button
            self.buttons[0].enabled = True

            # Create move option buttons
            self._create_move_buttons(action_space)
        else:
            self.available_moves = []
            self.buttons[0].enabled = False
            self.move_buttons = []

    def _create_move_buttons(self, action_space: "ActionSpace"):
        """Create buttons for each move option in the action space."""
        self.move_buttons = []

        for idx, action_choice in enumerate(action_space.action_set):
            if not action_choice:
                continue

            # Create a label for this action choice
            label = self._get_action_choice_label(action_choice, idx)

            # Create a callback that captures this action_choice
            def make_callback(ac: "ActionChoice"):
                def callback():
                    if self.on_move_selected:
                        self.on_move_selected(ac)
                return callback

            button = Button(
                pygame.Rect(0, 0, 120, BUTTON_HEIGHT - 4),
                label,
                make_callback(action_choice),
                enabled=True,
                color=Colors.PANEL_BORDER,
            )
            self.move_buttons.append(button)

        self._reposition_move_buttons()

    def _get_action_choice_label(self, action_choice: "ActionChoice", index: int) -> str:
        """Generate a short label for an action choice."""
        if not action_choice:
            return f"Option {index + 1}"

        # Get the first move option for the label
        first_move = action_choice[0]
        move_type = first_move.move_type
        target = first_move.move_target

        # Create a short readable label
        from game_env.moves.move_types import MoveType
        from game_env.regions_enum import R
        from game_env.characters import CompanionName

        # Type-specific formatting
        if target is None:
            return move_type.name.replace("_", " ").title()[:15]
        elif isinstance(target, R):
            return f"{target.name[:12]}"
        elif isinstance(target, CompanionName):
            return f"{target.name[:12]}"
        elif hasattr(target, 'idx'):
            # CardReference
            return f"Card {target.idx}"
        else:
            return f"#{index + 1}: {move_type.name[:10]}"

    def _reposition_move_buttons(self):
        """Position the move option buttons in the panel."""
        if not self.move_buttons:
            return

        # Position buttons in a row, starting from left side
        x = self.rect.x + BUTTON_PADDING
        y = self.rect.y + 5

        # Calculate how many buttons we can show
        visible_buttons = self.move_buttons[
            self.scroll_offset : self.scroll_offset + self.max_visible_buttons
        ]

        for button in visible_buttons:
            button.rect.x = x
            button.rect.y = y
            x += button.rect.width + 4

    def handle_scroll(self, direction: int):
        """Handle scrolling through move buttons."""
        if len(self.move_buttons) <= self.max_visible_buttons:
            return

        self.scroll_offset += direction
        self.scroll_offset = max(0, min(
            self.scroll_offset,
            len(self.move_buttons) - self.max_visible_buttons
        ))
        self._reposition_move_buttons()

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

        # Draw move option buttons if present
        if self.move_buttons:
            visible_buttons = self.move_buttons[
                self.scroll_offset : self.scroll_offset + self.max_visible_buttons
            ]
            for button in visible_buttons:
                button.draw(screen, font_small)

            # Draw scroll indicators if needed
            if len(self.move_buttons) > self.max_visible_buttons:
                if self.scroll_offset > 0:
                    # Left arrow indicator
                    arrow_left = font_small.render("<", True, Colors.TEXT_PRIMARY)
                    screen.blit(arrow_left, (self.rect.x + 2, self.rect.y + 8))
                if self.scroll_offset < len(self.move_buttons) - self.max_visible_buttons:
                    # Right arrow indicator
                    arrow_right = font_small.render(">", True, Colors.TEXT_PRIMARY)
                    # Position after the last visible button
                    if visible_buttons:
                        last_btn = visible_buttons[-1]
                        screen.blit(arrow_right, (last_btn.rect.right + 4, self.rect.y + 8))

            # Show count
            count_text = font_small.render(
                f"({len(self.move_buttons)} options)",
                True,
                Colors.TEXT_MUTED,
            )
            screen.blit(count_text, (self.rect.x + BUTTON_PADDING, self.rect.y + 35))
        else:
            # Draw message when no move buttons
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

        # Draw default control buttons
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
        # Check move option buttons first
        if self.move_buttons:
            visible_buttons = self.move_buttons[
                self.scroll_offset : self.scroll_offset + self.max_visible_buttons
            ]
            for button in visible_buttons:
                if button.handle_click(pos):
                    return True

        # Check default control buttons
        for button in self.buttons:
            if button.handle_click(pos):
                return True
        return False

    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """Handle mouse motion for hover effects."""
        # Handle move option buttons
        if self.move_buttons:
            visible_buttons = self.move_buttons[
                self.scroll_offset : self.scroll_offset + self.max_visible_buttons
            ]
            for button in visible_buttons:
                button.handle_motion(pos)

        # Handle default control buttons
        for button in self.buttons:
            button.handle_motion(pos)
