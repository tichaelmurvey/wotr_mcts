"""
Card panel component for War of the Ring interface.

Displays player's hand of cards as thumbnails with click-to-expand functionality.
"""

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple
import pygame

from pygame_interface.config import (
    Colors,
    CARD_THUMBNAIL_WIDTH,
    CARD_THUMBNAIL_HEIGHT,
    CARD_FULL_WIDTH,
    CARD_FULL_HEIGHT,
    FONT_SIZE_SMALL,
)
from pygame_interface.assets import get_asset_manager
from game_env.game_env_enums import Player

if TYPE_CHECKING:
    from game_env.event_cards.cards import EventCard


class CardPanel:
    """
    Panel for displaying and selecting cards from player hands.
    """

    def __init__(self, rect: pygame.Rect):
        """
        Initialize the card panel.

        Args:
            rect: The rectangle area for the card panel
        """
        self.rect = rect
        self.assets = get_asset_manager()

        # Current viewing player (whose cards are shown)
        self.active_player: Player = Player.FREE

        # Card hands
        self.free_hand: List["EventCard"] = []
        self.shadow_hand: List["EventCard"] = []

        # Card positions for click detection
        self.card_rects: List[pygame.Rect] = []

        # Selection state
        self.hovered_card_idx: Optional[int] = None
        self.selected_card_idx: Optional[int] = None
        self.expanded_card: Optional["EventCard"] = None

        # Scroll for many cards
        self.scroll_offset = 0

    def set_rect(self, rect: pygame.Rect):
        """Update the display rectangle."""
        self.rect = rect
        self._recalculate_card_positions()

    def set_hand(self, player: Player, cards: List["EventCard"]):
        """
        Set the cards in a player's hand.

        Args:
            player: Which player's hand
            cards: List of EventCard objects
        """
        if player == Player.FREE:
            self.free_hand = cards
        else:
            self.shadow_hand = cards

        if player == self.active_player:
            self._recalculate_card_positions()

    def set_active_player(self, player: Player):
        """Set which player's hand is displayed."""
        self.active_player = player
        self._recalculate_card_positions()

    def _recalculate_card_positions(self):
        """Recalculate card positions based on current hand."""
        self.card_rects.clear()

        hand = self.free_hand if self.active_player == Player.FREE else self.shadow_hand
        if not hand:
            return

        # Calculate spacing
        padding = 10
        available_width = self.rect.width - padding * 2
        card_spacing = min(
            CARD_THUMBNAIL_WIDTH + 5,
            (available_width - CARD_THUMBNAIL_WIDTH) // max(1, len(hand) - 1),
        )

        # Center the cards
        total_width = (len(hand) - 1) * card_spacing + CARD_THUMBNAIL_WIDTH
        start_x = self.rect.x + (self.rect.width - total_width) // 2

        y = self.rect.y + (self.rect.height - CARD_THUMBNAIL_HEIGHT) // 2

        for i in range(len(hand)):
            x = start_x + i * card_spacing - self.scroll_offset
            self.card_rects.append(pygame.Rect(
                x, y,
                CARD_THUMBNAIL_WIDTH,
                CARD_THUMBNAIL_HEIGHT,
            ))

    def get_card_at_pos(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Get the index of the card at a screen position.

        Args:
            pos: (x, y) screen position

        Returns:
            Card index or None
        """
        if not self.rect.collidepoint(pos):
            return None

        # Check in reverse order (topmost card first due to overlap)
        for i in range(len(self.card_rects) - 1, -1, -1):
            if self.card_rects[i].collidepoint(pos):
                return i

        return None

    def handle_click(self, pos: Tuple[int, int]) -> Optional["EventCard"]:
        """
        Handle a click on the card panel.

        Args:
            pos: (x, y) screen position

        Returns:
            The clicked EventCard or None
        """
        card_idx = self.get_card_at_pos(pos)
        if card_idx is None:
            self.selected_card_idx = None
            self.expanded_card = None
            return None

        hand = self.free_hand if self.active_player == Player.FREE else self.shadow_hand

        if card_idx < len(hand):
            if self.selected_card_idx == card_idx:
                # Double click - expand card
                self.expanded_card = hand[card_idx]
            else:
                self.selected_card_idx = card_idx
            return hand[card_idx]

        return None

    def close_expanded(self):
        """Close the expanded card view."""
        self.expanded_card = None

    def update(self):
        """Update card panel state."""
        pass

    def draw(self, screen: pygame.Surface):
        """Draw the card panel."""
        # Draw background
        pygame.draw.rect(screen, Colors.PANEL_BG, self.rect)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, self.rect, 2)

        # Draw player indicator
        self._draw_player_tabs(screen)

        # Draw cards
        self._draw_cards(screen)

        # Draw expanded card if any
        if self.expanded_card:
            self._draw_expanded_card(screen)

    def _draw_player_tabs(self, screen: pygame.Surface):
        """Draw tabs to switch between player hands."""
        font = self.assets.get_font(FONT_SIZE_SMALL)

        # Free Peoples tab
        fp_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 2, 80, 20)
        fp_color = Colors.FREE_PEOPLES if self.active_player == Player.FREE else Colors.DARK_GRAY
        pygame.draw.rect(screen, fp_color, fp_rect)
        fp_text = font.render("Free", True, Colors.WHITE)
        screen.blit(fp_text, (fp_rect.x + 5, fp_rect.y + 2))

        # Shadow tab
        shadow_rect = pygame.Rect(fp_rect.right + 5, self.rect.y + 2, 80, 20)
        shadow_color = Colors.SHADOW if self.active_player == Player.SHADOW else Colors.DARK_GRAY
        pygame.draw.rect(screen, shadow_color, shadow_rect)
        shadow_text = font.render("Shadow", True, Colors.WHITE)
        screen.blit(shadow_text, (shadow_rect.x + 5, shadow_rect.y + 2))

    def _draw_cards(self, screen: pygame.Surface):
        """Draw the card thumbnails."""
        hand = self.free_hand if self.active_player == Player.FREE else self.shadow_hand

        if not hand:
            # Draw empty hand message
            font = self.assets.get_font(FONT_SIZE_SMALL)
            text = font.render("No cards in hand", True, Colors.TEXT_MUTED)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)
            return

        # Draw each card
        for i, card in enumerate(hand):
            if i >= len(self.card_rects):
                break

            rect = self.card_rects[i]

            # Skip cards outside visible area
            if rect.right < self.rect.x or rect.x > self.rect.right:
                continue

            # Get card image
            card_image = self.assets.get_card_thumbnail(
                self.active_player,
                card.idx,
            )
            screen.blit(card_image, rect.topleft)

            # Draw selection highlight
            if i == self.selected_card_idx:
                pygame.draw.rect(screen, Colors.CARD_SELECTED, rect, 3)
            elif i == self.hovered_card_idx:
                pygame.draw.rect(screen, Colors.HIGHLIGHT_HOVER[:3], rect, 2)

    def _draw_expanded_card(self, screen: pygame.Surface):
        """Draw the expanded card view."""
        if not self.expanded_card:
            return

        # Get full card image
        card_image = self.assets.get_card_full(
            self.active_player,
            self.expanded_card.idx,
        )

        # Center on screen
        screen_rect = screen.get_rect()
        card_rect = card_image.get_rect(center=screen_rect.center)

        # Draw dimmed background
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Draw card
        screen.blit(card_image, card_rect)

        # Draw close hint
        font = self.assets.get_font(FONT_SIZE_SMALL)
        hint = font.render("Click anywhere to close", True, Colors.TEXT_SECONDARY)
        hint_rect = hint.get_rect(
            centerx=screen_rect.centerx,
            top=card_rect.bottom + 10,
        )
        screen.blit(hint, hint_rect)

    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """Handle mouse motion for hover effects."""
        self.hovered_card_idx = self.get_card_at_pos(pos)

    def handle_scroll(self, direction: int):
        """Handle scroll wheel for scrolling cards."""
        max_scroll = max(0, len(self.card_rects) * 30 - self.rect.width + 100)
        self.scroll_offset += direction * 30
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        self._recalculate_card_positions()
