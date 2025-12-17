"""
Sidebar component for War of the Ring interface.

Displays:
- Current phase and turn
- Action dice for both players
- Hunt box info
- Fellowship status
- Victory points
"""

from typing import List, Optional, Tuple
import pygame

from pygame_interface.config import (
    Colors,
    ACTION_DIE_SIZE,
    FONT_SIZE_LARGE,
    FONT_SIZE_MEDIUM,
    FONT_SIZE_SMALL,
)
from pygame_interface.assets import get_asset_manager
from game_env.game_env_enums import Player
from game_env.action_dice.dice import ActionResult


class Sidebar:
    """
    Sidebar panel displaying game status information.
    """

    def __init__(self, rect: pygame.Rect):
        """
        Initialize the sidebar.

        Args:
            rect: The rectangle area for the sidebar
        """
        self.rect = rect
        self.assets = get_asset_manager()

        # Phase info
        self.turn: int = 0
        self.phase: str = "Setup"

        # Dice info (list of (ActionResult, is_used) tuples)
        self.free_dice: List[Tuple[ActionResult, bool]] = []
        self.shadow_dice: List[Tuple[ActionResult, bool]] = []

        # Hunt box
        self.hunt_fp_dice: int = 0
        self.hunt_eyes: int = 0

        # Fellowship info
        self.fellowship_position: int = 0
        self.fellowship_corruption: int = 0
        self.fellowship_guide: Optional[str] = None
        self.fellowship_companions: List[str] = []
        self.fellowship_revealed: bool = False
        self.fellowship_in_mordor: bool = False

        # Player info
        self.free_cards: int = 0
        self.free_dice_available: int = 0
        self.shadow_cards: int = 0
        self.shadow_dice_available: int = 0

        # Table cards
        self.table_cards: List = []

        # Victory points
        self.free_vp: int = 0
        self.shadow_vp: int = 0

        # Scroll offset for content
        self.scroll_offset = 0

        # Current awaited move info
        self.awaited_move: Optional[str] = None

    def set_rect(self, rect: pygame.Rect):
        """Update the display rectangle."""
        self.rect = rect

    def set_phase_info(self, turn: int, phase: str):
        """Set the current turn and phase."""
        self.turn = turn
        self.phase = phase

    def set_free_dice(self, dice: List[Tuple[ActionResult, bool]]):
        """Set the Free Peoples dice results."""
        self.free_dice = dice

    def set_shadow_dice(self, dice: List[Tuple[ActionResult, bool]]):
        """Set the Shadow dice results."""
        self.shadow_dice = dice

    def set_hunt_box(self, fp_dice: int, eyes: int):
        """Set hunt box information."""
        self.hunt_fp_dice = fp_dice
        self.hunt_eyes = eyes

    def set_fellowship_info(
        self,
        position: int,
        corruption: int,
        guide: Optional[str],
        companions: List[str],
        revealed: bool,
        in_mordor: bool,
    ):
        """Set fellowship information."""
        self.fellowship_position = position
        self.fellowship_corruption = corruption
        self.fellowship_guide = guide
        self.fellowship_companions = companions
        self.fellowship_revealed = revealed
        self.fellowship_in_mordor = in_mordor

    def set_free_peoples_info(self, cards_in_hand: int, dice_available: int):
        """Set Free Peoples player info."""
        self.free_cards = cards_in_hand
        self.free_dice_available = dice_available

    def set_shadow_info(self, cards_in_hand: int, dice_available: int):
        """Set Shadow player info."""
        self.shadow_cards = cards_in_hand
        self.shadow_dice_available = dice_available

    def set_table_cards(self, cards: List):
        """Set cards currently on the table."""
        self.table_cards = cards

    def set_victory_points(self, free_vp: int, shadow_vp: int):
        """Set victory point totals."""
        self.free_vp = free_vp
        self.shadow_vp = shadow_vp

    def set_awaited_move(self, move_description: Optional[str]):
        """Set the description of the move currently being awaited."""
        self.awaited_move = move_description

    def update(self):
        """Update sidebar state."""
        pass

    def draw(self, screen: pygame.Surface):
        """Draw the sidebar to the screen."""
        # Draw background
        pygame.draw.rect(screen, Colors.PANEL_BG, self.rect)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, self.rect, 2)

        # Current y position for drawing
        y = self.rect.y + 10
        padding = 10
        section_spacing = 15

        # Draw phase info
        y = self._draw_phase_info(screen, y, padding)
        y += section_spacing

        # Draw Free Peoples section
        y = self._draw_player_section(
            screen, y, padding,
            "Free Peoples",
            Colors.FREE_PEOPLES,
            self.free_dice,
            Player.FREE,
            self.free_cards,
        )
        y += section_spacing

        # Draw Shadow section
        y = self._draw_player_section(
            screen, y, padding,
            "Shadow",
            Colors.SHADOW,
            self.shadow_dice,
            Player.SHADOW,
            self.shadow_cards,
        )
        y += section_spacing

        # Draw Hunt Box
        y = self._draw_hunt_box(screen, y, padding)
        y += section_spacing

        # Draw Fellowship info
        y = self._draw_fellowship_info(screen, y, padding)

    def _draw_phase_info(self, screen: pygame.Surface, y: int, padding: int) -> int:
        """Draw the turn and phase information."""
        font_large = self.assets.get_font(FONT_SIZE_LARGE)
        font_medium = self.assets.get_font(FONT_SIZE_MEDIUM)
        font_small = self.assets.get_font(FONT_SIZE_SMALL)

        # Turn number
        turn_text = font_large.render(f"Turn {self.turn}", True, Colors.TEXT_PRIMARY)
        screen.blit(turn_text, (self.rect.x + padding, y))
        y += turn_text.get_height() + 5

        # Phase
        phase_text = font_medium.render(self.phase, True, Colors.TEXT_SECONDARY)
        screen.blit(phase_text, (self.rect.x + padding, y))
        y += phase_text.get_height() + 3

        # Awaited move (if any)
        if self.awaited_move:
            awaited_text = font_small.render(
                f"Awaiting: {self.awaited_move}",
                True,
                Colors.TEXT_MUTED,
            )
            screen.blit(awaited_text, (self.rect.x + padding, y))
            y += awaited_text.get_height()

        return y

    def _draw_player_section(
        self,
        screen: pygame.Surface,
        y: int,
        padding: int,
        title: str,
        color: Tuple[int, int, int],
        dice: List[Tuple[ActionResult, bool]],
        player: Player,
        cards: int,
    ) -> int:
        """Draw a player's section with dice and info."""
        font_medium = self.assets.get_font(FONT_SIZE_MEDIUM)
        font_small = self.assets.get_font(FONT_SIZE_SMALL)

        # Section header
        header_rect = pygame.Rect(
            self.rect.x + padding,
            y,
            self.rect.width - padding * 2,
            24,
        )
        pygame.draw.rect(screen, color, header_rect)
        title_text = font_medium.render(title, True, Colors.WHITE)
        screen.blit(title_text, (header_rect.x + 5, header_rect.y + 2))
        y += header_rect.height + 5

        # Cards in hand
        cards_text = font_small.render(f"Cards: {cards}", True, Colors.TEXT_SECONDARY)
        screen.blit(cards_text, (self.rect.x + padding, y))
        y += cards_text.get_height() + 5

        # Dice
        if dice:
            x = self.rect.x + padding
            die_size = min(ACTION_DIE_SIZE, (self.rect.width - padding * 2) // len(dice) - 2)

            for result, used in dice:
                # Draw die image
                die_image = self.assets.get_action_die_image(player, result, die_size)
                screen.blit(die_image, (x, y))

                # Gray out if used
                if used:
                    overlay = pygame.Surface((die_size, die_size), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 150))
                    screen.blit(overlay, (x, y))

                x += die_size + 2

            y += die_size + 5

        return y

    def _draw_hunt_box(self, screen: pygame.Surface, y: int, padding: int) -> int:
        """Draw the hunt box information."""
        font_medium = self.assets.get_font(FONT_SIZE_MEDIUM)
        font_small = self.assets.get_font(FONT_SIZE_SMALL)

        # Header
        header_text = font_medium.render("Hunt Box", True, Colors.TEXT_PRIMARY)
        screen.blit(header_text, (self.rect.x + padding, y))
        y += header_text.get_height() + 5

        # FP dice in hunt
        fp_text = font_small.render(
            f"FP Dice: {self.hunt_fp_dice}",
            True,
            Colors.FREE_PEOPLES,
        )
        screen.blit(fp_text, (self.rect.x + padding, y))
        y += fp_text.get_height() + 3

        # Eyes
        eyes_text = font_small.render(
            f"Eyes: {self.hunt_eyes}",
            True,
            Colors.SHADOW,
        )
        screen.blit(eyes_text, (self.rect.x + padding, y))
        y += eyes_text.get_height()

        return y

    def _draw_fellowship_info(self, screen: pygame.Surface, y: int, padding: int) -> int:
        """Draw fellowship status information."""
        font_medium = self.assets.get_font(FONT_SIZE_MEDIUM)
        font_small = self.assets.get_font(FONT_SIZE_SMALL)

        # Header
        header_text = font_medium.render("Fellowship", True, Colors.TEXT_PRIMARY)
        screen.blit(header_text, (self.rect.x + padding, y))
        y += header_text.get_height() + 5

        # Status
        if self.fellowship_in_mordor:
            status = "In Mordor"
        elif self.fellowship_revealed:
            status = "Revealed"
        else:
            status = "Hidden"
        status_text = font_small.render(status, True, Colors.TEXT_SECONDARY)
        screen.blit(status_text, (self.rect.x + padding, y))
        y += status_text.get_height() + 3

        # Progress
        progress_text = font_small.render(
            f"Progress: {self.fellowship_position}",
            True,
            Colors.TEXT_SECONDARY,
        )
        screen.blit(progress_text, (self.rect.x + padding, y))
        y += progress_text.get_height() + 3

        # Corruption
        corruption_color = Colors.TEXT_SECONDARY
        if self.fellowship_corruption >= 8:
            corruption_color = Colors.SHADOW
        corruption_text = font_small.render(
            f"Corruption: {self.fellowship_corruption}/12",
            True,
            corruption_color,
        )
        screen.blit(corruption_text, (self.rect.x + padding, y))
        y += corruption_text.get_height() + 3

        # Guide
        if self.fellowship_guide:
            guide_text = font_small.render(
                f"Guide: {self.fellowship_guide}",
                True,
                Colors.TEXT_SECONDARY,
            )
            screen.blit(guide_text, (self.rect.x + padding, y))
            y += guide_text.get_height() + 3

        # Companion count
        companion_text = font_small.render(
            f"Companions: {len(self.fellowship_companions)}",
            True,
            Colors.TEXT_SECONDARY,
        )
        screen.blit(companion_text, (self.rect.x + padding, y))
        y += companion_text.get_height()

        return y

    def handle_scroll(self, direction: int):
        """Handle scroll wheel input."""
        self.scroll_offset += direction * 20
        self.scroll_offset = max(0, self.scroll_offset)
