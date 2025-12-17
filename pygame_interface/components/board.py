"""
Board rendering component for War of the Ring.

Handles:
- Loading and displaying the game board image
- Zoom and pan functionality
- Region highlighting
- Unit token rendering on regions
"""

from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple
from collections import Counter
import pygame

from pygame_interface.config import (
    Colors,
    DEFAULT_BOARD_SCALE,
    UNIT_TOKEN_SIZE,
    UNIT_TOKEN_SMALL,
)
from pygame_interface.assets import get_asset_manager
from game_env.regions_enum import R
from game_env.army import FreeUnit, ShadowUnit

if TYPE_CHECKING:
    from pygame_interface.components.regions import RegionManager


class Board:
    """
    Handles rendering of the game board including:
    - The board image with zoom/pan
    - Region highlighting
    - Unit tokens on regions
    - Fellowship marker
    """

    def __init__(
        self,
        rect: pygame.Rect,
        region_manager: "RegionManager",
    ):
        """
        Initialize the board component.

        Args:
            rect: The rectangle area for the board on screen
            region_manager: RegionManager for region data
        """
        self.rect = rect
        self.region_manager = region_manager
        self.assets = get_asset_manager()

        # Board image and transform
        self.board_scale = DEFAULT_BOARD_SCALE
        self.board_image: Optional[pygame.Surface] = None
        self._load_board()

        # Zoom and pan
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        self.pan_offset = [0, 0]  # [x, y] offset for panning
        self.is_panning = False
        self.pan_start = None

        # Highlighting
        self.highlighted_regions: Dict[R, Tuple[int, int, int, int]] = {}
        self.selected_region: Optional[R] = None
        self.hovered_region: Optional[R] = None

        # Unit data (set by state renderer)
        self.region_units: Dict[R, Counter] = {}
        self.region_characters: Dict[R, List[str]] = {}
        self.fellowship_region: Optional[R] = None
        self.fellowship_revealed: bool = False

        # Control markers
        self.region_control: Dict[R, int] = {}  # R -> Player value

        # Calculate initial zoom to fit board in rect
        self._fit_board_to_rect()

    def _load_board(self):
        """Load the board image."""
        self.board_image = self.assets.get_board(self.board_scale)

    def _fit_board_to_rect(self):
        """Calculate zoom to fit board in the display rect."""
        if self.board_image is None:
            return

        board_w, board_h = self.board_image.get_size()
        rect_w, rect_h = self.rect.width, self.rect.height

        # Calculate zoom to fit
        zoom_x = rect_w / board_w
        zoom_y = rect_h / board_h
        self.zoom = min(zoom_x, zoom_y)

        # Center the board
        scaled_w = board_w * self.zoom
        scaled_h = board_h * self.zoom
        self.pan_offset[0] = int((rect_w - scaled_w) / 2)
        self.pan_offset[1] = int((rect_h - scaled_h) / 2)

    def set_rect(self, rect: pygame.Rect):
        """Update the display rectangle (on resize)."""
        self.rect = rect
        self._fit_board_to_rect()

    def get_board_size(self) -> Tuple[int, int]:
        """Get the size of the board image."""
        if self.board_image is None:
            return (0, 0)
        return self.board_image.get_size()

    def screen_to_board_pos(
        self,
        screen_pos: Tuple[int, int],
    ) -> Optional[Tuple[int, int]]:
        """
        Convert screen coordinates to board image coordinates.

        Args:
            screen_pos: (x, y) screen coordinates

        Returns:
            (x, y) board coordinates, or None if outside board
        """
        if self.board_image is None:
            return None

        # Check if position is in board rect
        if not self.rect.collidepoint(screen_pos):
            return None

        # Convert to local rect coordinates
        local_x = screen_pos[0] - self.rect.x
        local_y = screen_pos[1] - self.rect.y

        # Apply inverse pan and zoom
        board_x = (local_x - self.pan_offset[0]) / self.zoom
        board_y = (local_y - self.pan_offset[1]) / self.zoom

        # Check bounds
        board_w, board_h = self.board_image.get_size()
        if 0 <= board_x < board_w and 0 <= board_y < board_h:
            return (int(board_x), int(board_y))

        return None

    def board_to_screen_pos(
        self,
        board_pos: Tuple[int, int],
    ) -> Tuple[int, int]:
        """
        Convert board image coordinates to screen coordinates.

        Args:
            board_pos: (x, y) board coordinates

        Returns:
            (x, y) screen coordinates
        """
        screen_x = board_pos[0] * self.zoom + self.pan_offset[0] + self.rect.x
        screen_y = board_pos[1] * self.zoom + self.pan_offset[1] + self.rect.y
        return (int(screen_x), int(screen_y))

    def set_zoom(self, zoom: float, center: Optional[Tuple[int, int]] = None):
        """
        Set the zoom level, optionally centering on a point.

        Args:
            zoom: New zoom level
            center: Optional screen position to zoom towards
        """
        old_zoom = self.zoom
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom))

        if center and self.zoom != old_zoom:
            # Adjust pan to keep the center point stationary
            local_x = center[0] - self.rect.x
            local_y = center[1] - self.rect.y

            # Point on board before zoom
            board_x = (local_x - self.pan_offset[0]) / old_zoom
            board_y = (local_y - self.pan_offset[1]) / old_zoom

            # Adjust pan to keep same board point under cursor
            self.pan_offset[0] = int(local_x - board_x * self.zoom)
            self.pan_offset[1] = int(local_y - board_y * self.zoom)

    def start_pan(self, pos: Tuple[int, int]):
        """Start panning from a position."""
        self.is_panning = True
        self.pan_start = pos

    def update_pan(self, pos: Tuple[int, int]):
        """Update pan position while dragging."""
        if self.is_panning and self.pan_start:
            dx = pos[0] - self.pan_start[0]
            dy = pos[1] - self.pan_start[1]
            self.pan_offset[0] += dx
            self.pan_offset[1] += dy
            self.pan_start = pos

    def end_pan(self):
        """End panning."""
        self.is_panning = False
        self.pan_start = None

    def highlight_region(self, region: R, color: Tuple[int, int, int, int]):
        """
        Highlight a region with a color.

        Args:
            region: R enum value of region to highlight
            color: RGBA color tuple
        """
        self.highlighted_regions[region] = color

    def set_highlighted_regions(
        self,
        regions: Set[R],
        color: Tuple[int, int, int, int],
    ):
        """
        Set multiple regions to be highlighted with same color.

        Args:
            regions: Set of R enum values
            color: RGBA color tuple
        """
        for region in regions:
            self.highlighted_regions[region] = color

    def clear_highlights(self):
        """Clear all region highlights."""
        self.highlighted_regions.clear()
        self.selected_region = None
        self.hovered_region = None

    def set_selected_region(self, region: Optional[R]):
        """Set the currently selected region."""
        self.selected_region = region

    def set_hovered_region(self, region: Optional[R]):
        """Set the currently hovered region."""
        self.hovered_region = region

    def set_region_units(self, region: R, units: Counter):
        """Set the units present in a region."""
        self.region_units[region] = units

    def set_region_characters(self, region: R, characters: List[str]):
        """Set the characters present in a region."""
        self.region_characters[region] = characters

    def set_fellowship(self, region: Optional[R], revealed: bool = False):
        """Set the fellowship location."""
        self.fellowship_region = region
        self.fellowship_revealed = revealed

    def set_region_control(self, region: R, player: int):
        """Set the control marker for a region."""
        self.region_control[region] = player

    def update(self):
        """Update board state (called each frame)."""
        pass

    def draw(self, screen: pygame.Surface):
        """
        Draw the board to the screen.

        Args:
            screen: The pygame surface to draw to
        """
        if self.board_image is None:
            return

        # Create a subsurface for the board area
        # First clip to the rect
        screen.set_clip(self.rect)

        # Calculate scaled board dimensions
        board_w, board_h = self.board_image.get_size()
        scaled_w = int(board_w * self.zoom)
        scaled_h = int(board_h * self.zoom)

        # Scale board image
        if self.zoom != 1.0:
            scaled_board = pygame.transform.smoothscale(
                self.board_image,
                (scaled_w, scaled_h),
            )
        else:
            scaled_board = self.board_image

        # Draw board
        board_x = self.rect.x + self.pan_offset[0]
        board_y = self.rect.y + self.pan_offset[1]
        screen.blit(scaled_board, (board_x, board_y))

        # Draw region highlights
        self._draw_highlights(screen)

        # Draw units on regions
        self._draw_units(screen)

        # Draw fellowship
        self._draw_fellowship(screen)

        # Draw hovered region name
        self._draw_hover_info(screen)

        # Reset clip
        screen.set_clip(None)

    def _draw_highlights(self, screen: pygame.Surface):
        """Draw region highlights."""
        board_size = self.get_board_size()

        # Draw highlighted regions
        for region, color in self.highlighted_regions.items():
            polygon = self.region_manager.get_polygon_for_drawing(region, board_size)
            if polygon:
                # Convert to screen coordinates
                screen_polygon = [self.board_to_screen_pos(p) for p in polygon]
                # Draw filled polygon with alpha
                self._draw_polygon_alpha(screen, screen_polygon, color)

        # Draw selected region
        if self.selected_region:
            polygon = self.region_manager.get_polygon_for_drawing(
                self.selected_region,
                board_size,
            )
            if polygon:
                screen_polygon = [self.board_to_screen_pos(p) for p in polygon]
                self._draw_polygon_alpha(
                    screen,
                    screen_polygon,
                    Colors.HIGHLIGHT_SELECTED,
                )

        # Draw hovered region
        if self.hovered_region and self.hovered_region != self.selected_region:
            polygon = self.region_manager.get_polygon_for_drawing(
                self.hovered_region,
                board_size,
            )
            if polygon:
                screen_polygon = [self.board_to_screen_pos(p) for p in polygon]
                self._draw_polygon_alpha(
                    screen,
                    screen_polygon,
                    Colors.HIGHLIGHT_HOVER,
                )

    def _draw_polygon_alpha(
        self,
        screen: pygame.Surface,
        polygon: List[Tuple[int, int]],
        color: Tuple[int, int, int, int],
    ):
        """Draw a polygon with alpha blending."""
        if len(polygon) < 3:
            return

        # Create a surface for the polygon
        min_x = min(p[0] for p in polygon)
        min_y = min(p[1] for p in polygon)
        max_x = max(p[0] for p in polygon)
        max_y = max(p[1] for p in polygon)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        if width <= 0 or height <= 0:
            return

        # Offset polygon to local coordinates
        local_polygon = [(p[0] - min_x, p[1] - min_y) for p in polygon]

        # Create surface with alpha
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(surface, color, local_polygon)

        # Blit to screen
        screen.blit(surface, (min_x, min_y))

    def _draw_units(self, screen: pygame.Surface):
        """Draw unit tokens on regions."""
        board_size = self.get_board_size()

        for region, units in self.region_units.items():
            if not units:
                continue

            center = self.region_manager.get_region_center(region, board_size)
            if center is None:
                continue

            screen_pos = self.board_to_screen_pos(center)
            self._draw_unit_stack(screen, screen_pos, units)

    def _draw_unit_stack(
        self,
        screen: pygame.Surface,
        pos: Tuple[int, int],
        units: Counter,
    ):
        """Draw a stack of unit tokens at a position."""
        # Determine base token size based on zoom
        base_token_size = int(UNIT_TOKEN_SIZE * min(self.zoom, 1.5))
        if base_token_size < UNIT_TOKEN_SMALL:
            base_token_size = UNIT_TOKEN_SMALL

        # Count total units for layout
        total_units = sum(units.values())
        if total_units == 0:
            return

        # Calculate layout - arrange in a grid pattern
        cols = min(3, total_units)
        # Use base size for spacing (elite units will overlap slightly, which looks fine)
        spacing = int(base_token_size * 0.7)

        x_start = pos[0] - (cols * spacing) // 2
        y_start = pos[1] - spacing // 2

        idx = 0
        for unit_type, count in units.items():
            for _ in range(count):
                row = idx // cols
                col = idx % cols

                x = x_start + col * spacing
                y = y_start + row * spacing

                # Get unit image (now preserves aspect ratio and handles elite sizing)
                image = self.assets.get_unit_image(unit_type, base_token_size)
                img_width, img_height = image.get_size()

                # Center the image at the grid position
                screen.blit(image, (x - img_width // 2, y - img_height // 2))

                idx += 1

    def _draw_fellowship(self, screen: pygame.Surface):
        """Draw the fellowship marker."""
        if self.fellowship_region is None:
            return

        board_size = self.get_board_size()
        center = self.region_manager.get_region_center(
            self.fellowship_region,
            board_size,
        )
        if center is None:
            return

        screen_pos = self.board_to_screen_pos(center)

        # Offset from center if there are units
        if self.fellowship_region in self.region_units:
            screen_pos = (screen_pos[0] + 20, screen_pos[1] - 20)

        token_size = int(UNIT_TOKEN_SIZE * min(self.zoom, 1.5))
        image = self.assets.get_fellowship_marker(
            self.fellowship_revealed,
            token_size,
        )
        screen.blit(
            image,
            (screen_pos[0] - token_size // 2, screen_pos[1] - token_size // 2),
        )

    def _draw_hover_info(self, screen: pygame.Surface):
        """Draw region name tooltip when hovering."""
        if self.hovered_region is None:
            return

        region_data = self.region_manager.get_region_by_enum(self.hovered_region)
        if region_data is None:
            return

        # Draw region name near bottom of board area
        font = self.assets.get_font(16)
        text = font.render(region_data.name, True, Colors.TEXT_PRIMARY)
        text_rect = text.get_rect(
            centerx=self.rect.centerx,
            bottom=self.rect.bottom - 5,
        )

        # Background
        padding = 5
        bg_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(screen, Colors.PANEL_BG, bg_rect)
        pygame.draw.rect(screen, Colors.PANEL_BORDER, bg_rect, 1)

        screen.blit(text, text_rect)
