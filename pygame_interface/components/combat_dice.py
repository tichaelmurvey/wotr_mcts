"""
Combat dice component for War of the Ring interface.

Handles rolling and displaying combat dice during battles.
"""

import random
import time
from typing import Callable, List, Optional, Tuple
import pygame

from pygame_interface.config import (
    Colors,
    COMBAT_DIE_SIZE,
    FONT_SIZE_MEDIUM,
    FONT_SIZE_SMALL,
)
from pygame_interface.assets import get_asset_manager


class CombatDice:
    """
    Combat dice roller and display component.

    Shows dice during combat with rolling animation and results.
    """

    def __init__(self):
        """Initialize the combat dice component."""
        self.assets = get_asset_manager()

        # State
        self.visible = False
        self.rect: Optional[pygame.Rect] = None

        # Dice values (1-6, with 6 representing a hit)
        self.dice_values: List[int] = []
        self.num_dice: int = 0
        self.hit_threshold: int = 6  # Value needed for a hit

        # Animation
        self.rolling = False
        self.roll_start_time: float = 0
        self.roll_duration: float = 1.0  # seconds
        self.animation_values: List[int] = []

        # Results
        self.hits: int = 0

        # Callback when rolling completes
        self.on_roll_complete: Optional[Callable[[List[int], int], None]] = None

    def show(self, rect: pygame.Rect, num_dice: int, hit_threshold: int = 6):
        """
        Show the dice roller.

        Args:
            rect: Rectangle to display in
            num_dice: Number of dice to roll
            hit_threshold: Value needed for a hit (default 6)
        """
        self.visible = True
        self.rect = rect
        self.num_dice = num_dice
        self.hit_threshold = hit_threshold
        self.dice_values = [1] * num_dice
        self.animation_values = [1] * num_dice
        self.rolling = False
        self.hits = 0

    def hide(self):
        """Hide the dice roller."""
        self.visible = False
        self.rolling = False

    def start_roll(self):
        """Start the dice rolling animation."""
        if self.rolling:
            return

        self.rolling = True
        self.roll_start_time = time.time()
        self.animation_values = [random.randint(1, 6) for _ in range(self.num_dice)]

    def _complete_roll(self):
        """Complete the roll and calculate results."""
        self.rolling = False
        self.dice_values = [random.randint(1, 6) for _ in range(self.num_dice)]
        self.hits = sum(1 for v in self.dice_values if v >= self.hit_threshold)

        if self.on_roll_complete:
            self.on_roll_complete(self.dice_values, self.hits)

    def set_results(self, values: List[int]):
        """
        Directly set dice results (for non-interactive display).

        Args:
            values: List of dice values
        """
        self.dice_values = values
        self.num_dice = len(values)
        self.hits = sum(1 for v in values if v >= self.hit_threshold)
        self.rolling = False

    def update(self):
        """Update animation state."""
        if not self.rolling:
            return

        elapsed = time.time() - self.roll_start_time

        if elapsed >= self.roll_duration:
            self._complete_roll()
        else:
            # Update animation values rapidly
            if random.random() < 0.3:  # Don't update every frame
                self.animation_values = [
                    random.randint(1, 6) for _ in range(self.num_dice)
                ]

    def draw(self, screen: pygame.Surface):
        """Draw the combat dice display."""
        if not self.visible or not self.rect:
            return

        # Draw background
        pygame.draw.rect(screen, Colors.DICE_BG, self.rect)
        pygame.draw.rect(screen, Colors.DICE_BORDER, self.rect, 2)

        font_medium = self.assets.get_font(FONT_SIZE_MEDIUM)
        font_small = self.assets.get_font(FONT_SIZE_SMALL)

        # Title
        title = font_medium.render("Combat Dice", True, Colors.TEXT_PRIMARY)
        screen.blit(title, (self.rect.x + 10, self.rect.y + 5))

        # Draw dice
        values = self.animation_values if self.rolling else self.dice_values
        self._draw_dice(screen, values)

        # Draw results if not rolling
        if not self.rolling and self.dice_values:
            result_text = f"Hits: {self.hits}"
            result_color = Colors.FREE_PEOPLES if self.hits > 0 else Colors.TEXT_MUTED
            result = font_medium.render(result_text, True, result_color)
            result_rect = result.get_rect(
                centerx=self.rect.centerx,
                bottom=self.rect.bottom - 10,
            )
            screen.blit(result, result_rect)

        # Draw roll button if not rolling
        if not self.rolling:
            self._draw_roll_button(screen)

    def _draw_dice(self, screen: pygame.Surface, values: List[int]):
        """Draw the dice with current values."""
        if not values or not self.rect:
            return

        # Calculate layout
        dice_per_row = min(5, len(values))
        spacing = COMBAT_DIE_SIZE + 5
        total_width = dice_per_row * spacing - 5

        start_x = self.rect.centerx - total_width // 2
        y = self.rect.y + 35

        for i, value in enumerate(values):
            row = i // dice_per_row
            col = i % dice_per_row

            x = start_x + col * spacing
            die_y = y + row * spacing

            self._draw_single_die(screen, x, die_y, value)

    def _draw_single_die(self, screen: pygame.Surface, x: int, y: int, value: int):
        """Draw a single die."""
        size = COMBAT_DIE_SIZE

        # Die background
        die_rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, Colors.WHITE, die_rect)
        pygame.draw.rect(screen, Colors.BLACK, die_rect, 2)

        # Draw pips based on value
        pip_color = Colors.BLACK
        pip_radius = size // 10

        # Pip positions (relative to die center)
        center = (x + size // 2, y + size // 2)
        offset = size // 4

        pip_positions = {
            1: [(0, 0)],
            2: [(-offset, -offset), (offset, offset)],
            3: [(-offset, -offset), (0, 0), (offset, offset)],
            4: [(-offset, -offset), (offset, -offset), (-offset, offset), (offset, offset)],
            5: [(-offset, -offset), (offset, -offset), (0, 0), (-offset, offset), (offset, offset)],
            6: [
                (-offset, -offset), (offset, -offset),
                (-offset, 0), (offset, 0),
                (-offset, offset), (offset, offset),
            ],
        }

        for dx, dy in pip_positions.get(value, []):
            pygame.draw.circle(
                screen,
                pip_color,
                (center[0] + dx, center[1] + dy),
                pip_radius,
            )

        # Highlight hits
        if value >= self.hit_threshold:
            pygame.draw.rect(screen, Colors.FREE_PEOPLES, die_rect, 3)

    def _draw_roll_button(self, screen: pygame.Surface):
        """Draw the roll button."""
        if not self.rect:
            return

        font = self.assets.get_font(FONT_SIZE_SMALL)

        button_width = 80
        button_height = 25
        button_rect = pygame.Rect(
            self.rect.centerx - button_width // 2,
            self.rect.bottom - 40,
            button_width,
            button_height,
        )

        pygame.draw.rect(screen, Colors.PANEL_BORDER, button_rect)
        pygame.draw.rect(screen, Colors.WHITE, button_rect, 1)

        text = font.render("Roll", True, Colors.TEXT_PRIMARY)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        self._roll_button_rect = button_rect

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """
        Handle a click on the dice component.

        Args:
            pos: (x, y) screen position

        Returns:
            True if click was handled
        """
        if not self.visible or not self.rect:
            return False

        if not self.rect.collidepoint(pos):
            return False

        # Check roll button
        if hasattr(self, "_roll_button_rect") and self._roll_button_rect.collidepoint(pos):
            if not self.rolling:
                self.start_roll()
            return True

        return True  # Consume click even if not on button


class CombatDiceOverlay:
    """
    Full-screen overlay for combat dice during battles.
    """

    def __init__(self, screen: pygame.Surface):
        """
        Initialize the overlay.

        Args:
            screen: The main screen surface
        """
        self.screen = screen
        self.assets = get_asset_manager()

        self.visible = False
        self.attacker_dice = CombatDice()
        self.defender_dice = CombatDice()

        self.attacker_name = "Attacker"
        self.defender_name = "Defender"

    def show(
        self,
        attacker_dice: int,
        defender_dice: int,
        attacker_name: str = "Attacker",
        defender_name: str = "Defender",
    ):
        """
        Show the combat overlay.

        Args:
            attacker_dice: Number of dice for attacker
            defender_dice: Number of dice for defender
            attacker_name: Display name for attacker
            defender_name: Display name for defender
        """
        self.visible = True
        self.attacker_name = attacker_name
        self.defender_name = defender_name

        screen_rect = self.screen.get_rect()
        panel_width = 200
        panel_height = 200
        gap = 40

        # Position dice panels
        attacker_rect = pygame.Rect(
            screen_rect.centerx - panel_width - gap // 2,
            screen_rect.centery - panel_height // 2,
            panel_width,
            panel_height,
        )
        defender_rect = pygame.Rect(
            screen_rect.centerx + gap // 2,
            screen_rect.centery - panel_height // 2,
            panel_width,
            panel_height,
        )

        self.attacker_dice.show(attacker_rect, attacker_dice)
        self.defender_dice.show(defender_rect, defender_dice)

    def hide(self):
        """Hide the overlay."""
        self.visible = False
        self.attacker_dice.hide()
        self.defender_dice.hide()

    def update(self):
        """Update dice animations."""
        if not self.visible:
            return
        self.attacker_dice.update()
        self.defender_dice.update()

    def draw(self):
        """Draw the overlay."""
        if not self.visible:
            return

        # Dim background
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font = self.assets.get_font(FONT_SIZE_MEDIUM)

        # Draw attacker label
        if self.attacker_dice.rect:
            label = font.render(self.attacker_name, True, Colors.FREE_PEOPLES)
            label_rect = label.get_rect(
                centerx=self.attacker_dice.rect.centerx,
                bottom=self.attacker_dice.rect.top - 5,
            )
            self.screen.blit(label, label_rect)

        # Draw defender label
        if self.defender_dice.rect:
            label = font.render(self.defender_name, True, Colors.SHADOW)
            label_rect = label.get_rect(
                centerx=self.defender_dice.rect.centerx,
                bottom=self.defender_dice.rect.top - 5,
            )
            self.screen.blit(label, label_rect)

        # Draw dice panels
        self.attacker_dice.draw(self.screen)
        self.defender_dice.draw(self.screen)

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        """Handle click on the overlay."""
        if not self.visible:
            return False

        if self.attacker_dice.handle_click(pos):
            return True
        if self.defender_dice.handle_click(pos):
            return True

        return True  # Consume all clicks when overlay is open
