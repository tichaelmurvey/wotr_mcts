"""
Reinforcement pool component for War of the Ring interface.

Displays available units for recruitment for both players.
"""

from typing import Dict, List, Optional, Tuple
from collections import Counter
import pygame

from pygame_interface.config import (
    Colors,
    UNIT_TOKEN_SIZE,
    UNIT_TOKEN_SMALL,
    FONT_SIZE_SMALL,
    FONT_SIZE_TINY,
    MAX_UNITS,
)
from pygame_interface.assets import get_asset_manager
from game_env.game_env_enums import Player
from game_env.army import ArmyUnit, ArmyUnit, ArmyUnit


# Unit groupings by nation for display
FREE_NATIONS = {
    "North": [ArmyUnit.nort_reg, ArmyUnit.nort_elt, ArmyUnit.nort_ldr],
    "Elves": [ArmyUnit.elvn_reg, ArmyUnit.elvn_elt, ArmyUnit.elvn_ldr],
    "Dwarves": [ArmyUnit.dwar_reg, ArmyUnit.dwar_elt, ArmyUnit.dwar_ldr],
    "Rohan": [ArmyUnit.rohn_reg, ArmyUnit.rohn_elt, ArmyUnit.rohn_ldr],
    "Gondor": [ArmyUnit.gond_reg, ArmyUnit.gond_elt, ArmyUnit.gond_ldr],
}

SHADOW_NATIONS = {
    "Isengard": [ArmyUnit.isen_reg, ArmyUnit.isen_elt],
    "Mordor": [ArmyUnit.mord_reg, ArmyUnit.mord_elt],
    "Easterlings": [ArmyUnit.east_reg, ArmyUnit.east_elt],
}


class ReinforcementPool:
    """
    Displays available reinforcement units for both players.

    This component is typically shown in the sidebar or as a popup
    during mustering actions.
    """

    def __init__(self):
        """Initialize the reinforcement pool display."""
        self.assets = get_asset_manager()

        # Available units (not yet on board)
        self.free_available: Dict[ArmyUnit, int] = {}
        self.shadow_available: Dict[ArmyUnit, int] = {}

        # Initialize with max units
        self._init_max_units()

        # Display state
        self.visible = False
        self.rect: Optional[pygame.Rect] = None
        self.active_player: Player = Player.FREE

        # Selection for mustering
        self.selected_unit: Optional[ArmyUnit] = None
        self.unit_rects: Dict[ArmyUnit, pygame.Rect] = {}

    def _init_max_units(self):
        """Initialize with maximum available units."""
        # Free Peoples
        self.free_available = {
            ArmyUnit.nort_reg: MAX_UNITS["north"]["regular"],
            ArmyUnit.nort_elt: MAX_UNITS["north"]["elite"],
            ArmyUnit.nort_ldr: MAX_UNITS["north"]["leader"],
            ArmyUnit.elvn_reg: MAX_UNITS["elves"]["regular"],
            ArmyUnit.elvn_elt: MAX_UNITS["elves"]["elite"],
            ArmyUnit.elvn_ldr: MAX_UNITS["elves"]["leader"],
            ArmyUnit.dwar_reg: MAX_UNITS["dwarves"]["regular"],
            ArmyUnit.dwar_elt: MAX_UNITS["dwarves"]["elite"],
            ArmyUnit.dwar_ldr: MAX_UNITS["dwarves"]["leader"],
            ArmyUnit.rohn_reg: MAX_UNITS["rohan"]["regular"],
            ArmyUnit.rohn_elt: MAX_UNITS["rohan"]["elite"],
            ArmyUnit.rohn_ldr: MAX_UNITS["rohan"]["leader"],
            ArmyUnit.gond_reg: MAX_UNITS["gondor"]["regular"],
            ArmyUnit.gond_elt: MAX_UNITS["gondor"]["elite"],
            ArmyUnit.gond_ldr: MAX_UNITS["gondor"]["leader"],
        }

        # Shadow
        self.shadow_available = {
            ArmyUnit.isen_reg: MAX_UNITS["isengard"]["regular"],
            ArmyUnit.isen_elt: MAX_UNITS["isengard"]["elite"],
            ArmyUnit.mord_reg: MAX_UNITS["mordor"]["regular"],
            ArmyUnit.mord_elt: MAX_UNITS["mordor"]["elite"],
            ArmyUnit.east_reg: MAX_UNITS["easterlings"]["regular"],
            ArmyUnit.east_elt: MAX_UNITS["easterlings"]["elite"],
        }

    def set_available_units(
        self,
        player: Player,
        available: Dict,
    ):
        """
        Set the available units for a player.

        Args:
            player: Which player
            available: Dict mapping unit type to count
        """
        if player == Player.FREE:
            self.free_available = available
        else:
            self.shadow_available = available

    def update_from_board(
        self,
        units_on_board: Counter,
        player: Player,
    ):
        """
        Update available units by subtracting units on board.

        Args:
            units_on_board: Counter of all units currently on the board
            player: Which player's units
        """
        if player == Player.FREE:
            max_units = self.free_available.copy()
            self._init_max_units()  # Reset to max
            for unit, count in units_on_board.items():
                if unit in self.free_available:
                    self.free_available[unit] = max(
                        0,
                        self.free_available.get(unit, 0) - count,
                    )
        else:
            max_units = self.shadow_available.copy()
            self._init_max_units()  # Reset to max
            for unit, count in units_on_board.items():
                if unit in self.shadow_available:
                    self.shadow_available[unit] = max(
                        0,
                        self.shadow_available.get(unit, 0) - count,
                    )

    def show(self, rect: pygame.Rect, player: Player):
        """
        Show the reinforcement pool for a player.

        Args:
            rect: Rectangle to display in
            player: Which player's pool to show
        """
        self.visible = True
        self.rect = rect
        self.active_player = player
        self._recalculate_unit_positions()

    def hide(self):
        """Hide the reinforcement pool."""
        self.visible = False
        self.selected_unit = None

    def _recalculate_unit_positions(self):
        """Recalculate clickable areas for each unit type."""
        if not self.rect:
            return

        self.unit_rects.clear()
        nations = FREE_NATIONS if self.active_player == Player.FREE else SHADOW_NATIONS

        y = self.rect.y + 30  # After header
        padding = 5
        token_size = UNIT_TOKEN_SMALL

        for nation_name, units in nations.items():
            y += 20  # Nation header

            x = self.rect.x + padding
            for unit in units:
                self.unit_rects[unit] = pygame.Rect(x, y, token_size, token_size)
                x += token_size + 25  # Space for count

            y += token_size + padding

    def get_unit_at_pos(self, pos: Tuple[int, int]) -> Optional[ArmyUnit]:
        """
        Get the unit type at a screen position.

        Args:
            pos: (x, y) screen position

        Returns:
            Unit type or None
        """
        for unit, rect in self.unit_rects.items():
            if rect.collidepoint(pos):
                return unit
        return None

    def handle_click(self, pos: Tuple[int, int]) -> Optional[ArmyUnit]:
        """
        Handle a click on the pool.

        Args:
            pos: (x, y) screen position

        Returns:
            Selected unit type or None
        """
        unit : ArmyUnit | None = self.get_unit_at_pos(pos) # type: ignore
        if unit:
            available : Dict[ArmyUnit, int] = (
                self.free_available if self.active_player == Player.FREE
                else self.shadow_available
            ) # type: ignore
            if available.get(unit, 0) > 0:
                self.selected_unit = unit
                return unit
        return None

    def draw(self, screen: pygame.Surface):
        """Draw the reinforcement pool."""
        if not self.visible or not self.rect:
            return

        # Draw background
        pygame.draw.rect(screen, Colors.PANEL_BG, self.rect)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, self.rect, 2)

        font_small = self.assets.get_font(FONT_SIZE_SMALL)
        font_tiny = self.assets.get_font(FONT_SIZE_TINY)

        # Header
        title = "Free Peoples Reinforcements" if self.active_player == Player.FREE else "Shadow Reinforcements"
        header_color = Colors.FREE_PEOPLES if self.active_player == Player.FREE else Colors.SHADOW
        title_text = font_small.render(title, True, header_color)
        screen.blit(title_text, (self.rect.x + 5, self.rect.y + 5))

        # Draw nations and units
        available = (
            self.free_available if self.active_player == Player.FREE
            else self.shadow_available
        )
        nations = FREE_NATIONS if self.active_player == Player.FREE else SHADOW_NATIONS

        y = self.rect.y + 30

        for nation_name, units in nations.items():
            # Nation header
            nation_text = font_tiny.render(nation_name, True, Colors.TEXT_SECONDARY)
            screen.blit(nation_text, (self.rect.x + 5, y))
            y += 18

            x = self.rect.x + 5
            for unit in units:
                count = available.get(unit, 0)

                # Draw unit image
                image = self.assets.get_unit_image(unit, UNIT_TOKEN_SMALL)
                screen.blit(image, (x, y))

                # Highlight if selected
                if unit == self.selected_unit:
                    pygame.draw.rect(
                        screen,
                        Colors.CARD_SELECTED,
                        (x - 2, y - 2, UNIT_TOKEN_SMALL + 4, UNIT_TOKEN_SMALL + 4),
                        2,
                    )

                # Gray out if none available
                if count == 0:
                    overlay = pygame.Surface(
                        (UNIT_TOKEN_SMALL, UNIT_TOKEN_SMALL),
                        pygame.SRCALPHA,
                    )
                    overlay.fill((0, 0, 0, 180))
                    screen.blit(overlay, (x, y))

                # Draw count
                count_text = font_tiny.render(str(count), True, Colors.TEXT_PRIMARY)
                screen.blit(count_text, (x + UNIT_TOKEN_SMALL + 2, y + 2))

                x += UNIT_TOKEN_SMALL + 25

            y += UNIT_TOKEN_SMALL + 5

    def draw_compact(self, screen: pygame.Surface, rect: pygame.Rect, player: Player):
        """
        Draw a compact version of the pool (for sidebar).

        Args:
            screen: Surface to draw on
            rect: Rectangle to draw in
            player: Which player's pool
        """
        available = self.free_available if player == Player.FREE else self.shadow_available
        nations = FREE_NATIONS if player == Player.FREE else SHADOW_NATIONS

        font_tiny = self.assets.get_font(FONT_SIZE_TINY)
        token_size = UNIT_TOKEN_SMALL - 4

        y = rect.y
        for nation_name, units in nations.items():
            x = rect.x
            for unit in units:
                count = available.get(unit, 0)
                if count > 0:
                    image = self.assets.get_unit_image(unit, token_size)
                    screen.blit(image, (x, y))
                    count_text = font_tiny.render(str(count), True, Colors.TEXT_SECONDARY)
                    screen.blit(count_text, (x + token_size - 2, y))
                    x += token_size + 12

            if x > rect.x:  # If any units were drawn
                y += token_size + 2

            if y > rect.bottom:
                break
