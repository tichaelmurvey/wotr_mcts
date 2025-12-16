"""
Asset loading and caching for the War of the Ring pygame interface.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import pygame

from pygame_interface.config import (
    IMAGES_DIR,
    CARDS_DIR,
    SMALLCARDS_DIR,
    UNITS_DIR,
    UNIT_IMAGES,
    CHARACTER_IMAGES,
    ACTION_DICE_IMAGES,
    SIEGE_OVERLAYS,
    CONTROL_MARKERS,
    FELLOWSHIP_IMAGE,
    FELLOWSHIP_REVEALED_IMAGE,
    UNIT_TOKEN_SIZE,
    ACTION_DIE_SIZE,
    CARD_THUMBNAIL_WIDTH,
    CARD_THUMBNAIL_HEIGHT,
    CARD_FULL_WIDTH,
    CARD_FULL_HEIGHT,
    get_board_image_path,
)
from game_env.army import ArmyUnit, FreeUnit, ShadowUnit
from game_env.action_dice.dice import ActionResult
from game_env.game_env_enums import Player
from game_env.regions_enum import R


class AssetManager:
    """
    Manages loading and caching of all game assets (images, fonts, sounds).
    Uses lazy loading - assets are only loaded when first requested.
    """

    def __init__(self):
        self._image_cache: Dict[str, pygame.Surface] = {}
        self._font_cache: Dict[Tuple[str, int], pygame.font.Font] = {}
        self._board_image: Optional[pygame.Surface] = None
        self._board_scale: int = 0

    def clear_cache(self):
        """Clear all cached assets."""
        self._image_cache.clear()
        self._font_cache.clear()
        self._board_image = None
        self._board_scale = 0

    def _load_image(
        self,
        path: Path,
        size: Optional[Tuple[int, int]] = None,
        alpha: bool = True,
    ) -> pygame.Surface:
        """
        Load an image from disk, optionally resizing it.

        Args:
            path: Path to the image file
            size: Optional (width, height) to scale the image to
            alpha: Whether to convert with alpha channel

        Returns:
            Loaded pygame Surface
        """
        cache_key = f"{path}_{size}_{alpha}"

        if cache_key in self._image_cache:
            return self._image_cache[cache_key]

        try:
            image = pygame.image.load(str(path))
            if alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()

            if size:
                image = pygame.transform.smoothscale(image, size)

            self._image_cache[cache_key] = image
            return image

        except pygame.error as e:
            print(f"Warning: Could not load image {path}: {e}")
            # Return a placeholder surface
            surface = pygame.Surface(size or (32, 32))
            surface.fill((255, 0, 255))  # Magenta for missing textures
            return surface

    def get_board(self, scale: int = 140, variant: str = "") -> pygame.Surface:
        """
        Load the game board image.

        Args:
            scale: Board scale percentage (80-200)
            variant: Optional variant suffix (e.g., "W")

        Returns:
            Board image as pygame Surface
        """
        if self._board_image is not None and self._board_scale == scale:
            return self._board_image

        path = get_board_image_path(scale, variant)
        self._board_image = self._load_image(path, alpha=False)
        self._board_scale = scale
        return self._board_image

    def get_unit_image(
        self,
        unit: ArmyUnit,
        size: int = UNIT_TOKEN_SIZE,
    ) -> pygame.Surface:
        """
        Get the image for a unit type.

        Args:
            unit: The unit type
            size: Size to scale the image to (square)

        Returns:
            Unit image as pygame Surface
        """
        filename = UNIT_IMAGES.get(unit)
        if not filename:
            print(f"Warning: No image mapping for unit {unit}")
            surface = pygame.Surface((size, size))
            surface.fill((255, 0, 255))
            return surface

        path = UNITS_DIR / filename
        return self._load_image(path, (size, size))

    def get_character_image(
        self,
        character_key: str,
        size: int = UNIT_TOKEN_SIZE,
    ) -> pygame.Surface:
        """
        Get the image for a character.

        Args:
            character_key: Character identifier (e.g., "gandalf_grey", "saruman")
            size: Size to scale the image to (square)

        Returns:
            Character image as pygame Surface
        """
        filename = CHARACTER_IMAGES.get(character_key)
        if not filename:
            print(f"Warning: No image mapping for character {character_key}")
            surface = pygame.Surface((size, size))
            surface.fill((255, 0, 255))
            return surface

        path = UNITS_DIR / filename
        return self._load_image(path, (size, size))

    def get_fellowship_marker(
        self,
        revealed: bool = False,
        size: int = UNIT_TOKEN_SIZE,
    ) -> pygame.Surface:
        """
        Get the fellowship marker image.

        Args:
            revealed: Whether the fellowship is revealed
            size: Size to scale the image to (square)

        Returns:
            Fellowship marker as pygame Surface
        """
        filename = FELLOWSHIP_REVEALED_IMAGE if revealed else FELLOWSHIP_IMAGE
        path = UNITS_DIR / filename
        return self._load_image(path, (size, size))

    def get_action_die_image(
        self,
        player: Player,
        result: ActionResult,
        size: int = ACTION_DIE_SIZE,
    ) -> pygame.Surface:
        """
        Get the image for an action die result.

        Args:
            player: Which player's die (FREE or SHADOW)
            result: The die result
            size: Size to scale the image to (square)

        Returns:
            Die image as pygame Surface
        """
        player_dice = ACTION_DICE_IMAGES.get(player, {})
        filename = player_dice.get(result)

        if not filename:
            print(f"Warning: No image mapping for {player} die result {result}")
            surface = pygame.Surface((size, size))
            surface.fill((255, 0, 255))
            return surface

        path = IMAGES_DIR / filename
        return self._load_image(path, (size, size))

    def get_card_thumbnail(
        self,
        player: Player,
        card_idx: int,
    ) -> pygame.Surface:
        """
        Get a card thumbnail image.

        Args:
            player: Which player's card (FREE or SHADOW)
            card_idx: Card index (1-52)

        Returns:
            Card thumbnail as pygame Surface
        """
        prefix = "fp" if player == Player.FREE else "sa"
        filename = f"{prefix}{card_idx:03d}.png"
        path = SMALLCARDS_DIR / filename
        return self._load_image(
            path,
            (CARD_THUMBNAIL_WIDTH, CARD_THUMBNAIL_HEIGHT),
        )

    def get_card_full(
        self,
        player: Player,
        card_idx: int,
    ) -> pygame.Surface:
        """
        Get a full-size card image.

        Args:
            player: Which player's card (FREE or SHADOW)
            card_idx: Card index (1-52)

        Returns:
            Full card image as pygame Surface
        """
        prefix = "fp" if player == Player.FREE else "sa"
        filename = f"{prefix}{card_idx:03d}.png"
        path = CARDS_DIR / filename
        return self._load_image(
            path,
            (CARD_FULL_WIDTH, CARD_FULL_HEIGHT),
        )

    def get_card_back(
        self,
        player: Player,
        deck_type: str = "character",
    ) -> pygame.Surface:
        """
        Get a card back image.

        Args:
            player: Which player's card back (FREE or SHADOW)
            deck_type: "character" or "strategy"

        Returns:
            Card back image as pygame Surface
        """
        if player == Player.FREE:
            filename = "FPCC.jpg" if deck_type == "character" else "FPAC.jpg"
        else:
            filename = "SACC.jpg" if deck_type == "character" else "SAAC.jpg"

        path = IMAGES_DIR / filename
        return self._load_image(path, (CARD_THUMBNAIL_WIDTH, CARD_THUMBNAIL_HEIGHT))

    def get_siege_overlay(
        self,
        region: R,
    ) -> Optional[pygame.Surface]:
        """
        Get the siege overlay image for a region.

        Args:
            region: The region enum value

        Returns:
            Siege overlay image or None if region doesn't have one
        """
        filename = SIEGE_OVERLAYS.get(region)
        if not filename:
            return None

        path = IMAGES_DIR / filename
        return self._load_image(path)

    def get_control_marker(
        self,
        player: Player,
        size: int = 24,
    ) -> pygame.Surface:
        """
        Get a control marker image.

        Args:
            player: Which player's control marker
            size: Size to scale the image to (square)

        Returns:
            Control marker as pygame Surface
        """
        filename = CONTROL_MARKERS.get(player)
        if not filename:
            surface = pygame.Surface((size, size))
            surface.fill((255, 0, 255))
            return surface

        path = IMAGES_DIR / filename
        return self._load_image(path, (size, size))

    def get_font(
        self,
        size: int,
        name: Optional[str] = None,
    ) -> pygame.font.Font:
        """
        Get a font, caching it for reuse.

        Args:
            size: Font size in points
            name: Optional font name (uses system default if None)

        Returns:
            pygame Font object
        """
        if name:
            cache_key = (name, size)
            if cache_key in self._font_cache:
                return self._font_cache[cache_key]
        
        try:
            if name:
                font = pygame.font.SysFont(name, size)
                self._font_cache[(name, size)] = font
            else:
                font = pygame.font.Font(None, size)
        except pygame.error:
            font = pygame.font.Font(None, size)

        return font

    def get_vp_marker(self, player: Player) -> pygame.Surface:
        """Get victory point marker for a player."""
        filename = "vp_free.png" if player == Player.FREE else "vp_shadow.png"
        path = IMAGES_DIR / filename
        if path.exists():
            return self._load_image(path, (24, 24))
        # Fallback - create a colored marker
        surface = pygame.Surface((24, 24), pygame.SRCALPHA)
        color = (70, 130, 180) if player == Player.FREE else (139, 69, 69)
        pygame.draw.circle(surface, color, (12, 12), 10)
        return surface

    def get_corruption_marker(self) -> pygame.Surface:
        """Get the corruption track marker."""
        # Create a simple marker if image doesn't exist
        surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(surface, (139, 69, 69), (10, 10), 8)
        pygame.draw.circle(surface, (0, 0, 0), (10, 10), 8, 2)
        return surface


# Global asset manager instance
_asset_manager: Optional[AssetManager] = None


def get_asset_manager() -> AssetManager:
    """Get the global AssetManager instance, creating it if necessary."""
    global _asset_manager
    if _asset_manager is None:
        _asset_manager = AssetManager()
    return _asset_manager


def init_assets():
    """Initialize the asset manager. Call after pygame.init()."""
    global _asset_manager
    _asset_manager = AssetManager()
    return _asset_manager
