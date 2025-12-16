"""
Region management for the War of the Ring interface.

Handles loading region polygon data, hit detection, and region-to-enum mapping.
"""

import json
from math import inf
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from pygame_interface.config import (
    REGIONS_JSON,
    REGION_JSON_TO_ENUM,
    REGION_ENUM_TO_JSON,
)
from game_env.regions_enum import R


@dataclass
class RegionData:
    """Data for a single region."""

    json_id: int
    name: str
    parent_id: int
    polygon: List[Tuple[float, float]]  # List of (x%, y%) points
    is_stronghold: bool
    is_city: bool
    is_town: bool
    is_fortification: bool
    r_enum: Optional[R]  # Corresponding R enum value

    @property
    def has_settlement(self) -> bool:
        """Check if region has any settlement type."""
        return self.is_stronghold or self.is_city or self.is_town

    def get_center(self) -> Tuple[float, float]:
        """
        Calculate the centroid of the polygon.

        Returns:
            (x%, y%) center point as percentages
        """
        if not self.polygon:
            return (50.0, 50.0)

        x_sum = sum(p[0] for p in self.polygon)
        y_sum = sum(p[1] for p in self.polygon)
        n = len(self.polygon)
        return (x_sum / n, y_sum / n)

    def get_pixel_polygon(
        self,
        board_width: int,
        board_height: int,
    ) -> List[Tuple[int, int]]:
        """
        Convert percentage polygon to pixel coordinates.

        Args:
            board_width: Width of the board image in pixels
            board_height: Height of the board image in pixels

        Returns:
            List of (x, y) pixel coordinates
        """
        return [
            (int(p[0] * board_width / 100), int(p[1] * board_height / 100))
            for p in self.polygon
        ]

    def get_pixel_center(
        self,
        board_width: int,
        board_height: int,
    ) -> Tuple[int, int]:
        """
        Get the center point in pixel coordinates.

        Args:
            board_width: Width of the board image in pixels
            board_height: Height of the board image in pixels

        Returns:
            (x, y) pixel coordinates of center
        """
        cx, cy = self.get_center()
        return (int(cx * board_width / 100), int(cy * board_height / 100))


@dataclass
class NationData:
    """Data for a nation grouping."""

    json_id: int
    name: str
    color: str
    is_shadow: bool
    regions: List[RegionData]


class RegionManager:
    """
    Manages region data and provides region lookup functionality.
    """

    def __init__(self):
        self.nations: Dict[int, NationData] = {}
        self.regions_by_json_id: Dict[int, RegionData] = {}
        self.regions_by_enum: Dict[R, RegionData] = {}

        self._load_regions()

    def _load_regions(self):
        """Load region data from JSON file."""
        try:
            with open(REGIONS_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Could not find {REGIONS_JSON}")
            return
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse {REGIONS_JSON}: {e}")
            return

        for nation_data in data:
            nation = NationData(
                json_id=nation_data["id"],
                name=nation_data["name"],
                color=nation_data["color"],
                is_shadow=nation_data["isShadows"],
                regions=[],
            )

            for region_data in nation_data.get("regions", []):
                polygon = self._parse_polygon(region_data.get("path", ""))

                # Get corresponding R enum value
                json_id = region_data["id"]
                r_enum = REGION_JSON_TO_ENUM.get(json_id)

                region = RegionData(
                    json_id=json_id,
                    name=region_data["name"],
                    parent_id=region_data["parentId"],
                    polygon=polygon,
                    is_stronghold=region_data.get("isStronghold", False),
                    is_city=region_data.get("isCity", False),
                    is_town=region_data.get("isTown", False),
                    is_fortification=region_data.get("isFortification", False),
                    r_enum=r_enum,
                )

                nation.regions.append(region)
                self.regions_by_json_id[json_id] = region

                if r_enum is not None:
                    self.regions_by_enum[r_enum] = region

            self.nations[nation.json_id] = nation

    def _parse_polygon(self, path: str) -> List[Tuple[float, float]]:
        """
        Parse a CSS polygon() string into a list of percentage coordinates.

        Args:
            path: CSS polygon string like "polygon(18% 21%, 18% 24%, ...)"

        Returns:
            List of (x%, y%) tuples
        """
        if not path or not path.startswith("polygon("):
            return []

        # Extract the content inside polygon()
        match = re.match(r"polygon\((.*)\)", path)
        if not match:
            return []

        content = match.group(1)
        points = []

        # Parse each point
        for point_str in content.split(","):
            point_str = point_str.strip()
            parts = point_str.split()
            if len(parts) >= 2:
                try:
                    x = float(parts[0].replace("%", ""))
                    y = float(parts[1].replace("%", ""))
                    points.append((x, y))
                except ValueError:
                    continue

        return points

    def get_region_by_enum(self, r: R) -> Optional[RegionData]:
        """
        Get region data by R enum value.

        Args:
            r: The R enum value

        Returns:
            RegionData or None if not found
        """
        return self.regions_by_enum.get(r)

    def get_region_by_json_id(self, json_id: int) -> Optional[RegionData]:
        """
        Get region data by JSON ID.

        Args:
            json_id: The JSON region ID

        Returns:
            RegionData or None if not found
        """
        return self.regions_by_json_id.get(json_id)

    def get_region_at_pos(
        self,
        pos: Tuple[int, int],
        board_size: Tuple[int, int],
    ) -> Optional[R]:
        """
        Get the region at a given pixel position.

        Args:
            pos: (x, y) pixel position on the board
            board_size: (width, height) of the board image

        Returns:
            R enum value of the region at that position, or None
        """
        board_width, board_height = board_size

        for region in self.regions_by_json_id.values():
            if region.r_enum is None:
                continue

            pixel_polygon = region.get_pixel_polygon(board_width, board_height)
            if self._point_in_polygon(pos, pixel_polygon):
                return region.r_enum

        return None

    def _point_in_polygon(
        self,
        point: Tuple[int, int],
        polygon: List[Tuple[int, int]],
    ) -> bool:
        """
        Check if a point is inside a polygon using ray casting algorithm.

        Args:
            point: (x, y) point to test
            polygon: List of (x, y) polygon vertices

        Returns:
            True if point is inside polygon
        """
        if len(polygon) < 3:
            return False

        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]

            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        xinters = -inf
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or (x <= xinters):
                            inside = not inside

            p1x, p1y = p2x, p2y

        return inside

    def get_region_center(
        self,
        r: R,
        board_size: Tuple[int, int],
    ) -> Optional[Tuple[int, int]]:
        """
        Get the center point of a region in pixel coordinates.

        Args:
            r: The R enum value
            board_size: (width, height) of the board image

        Returns:
            (x, y) pixel coordinates of region center, or None
        """
        region = self.regions_by_enum.get(r)
        if region is None:
            return None

        return region.get_pixel_center(board_size[0], board_size[1])

    def get_all_regions(self) -> List[RegionData]:
        """Get all region data objects."""
        return list(self.regions_by_json_id.values())

    def get_regions_for_nation(self, nation_id: int) -> List[RegionData]:
        """
        Get all regions belonging to a nation.

        Args:
            nation_id: The nation JSON ID

        Returns:
            List of RegionData for that nation
        """
        nation = self.nations.get(nation_id)
        if nation is None:
            return []
        return nation.regions

    def get_polygon_for_drawing(
        self,
        r: R,
        board_size: Tuple[int, int],
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Get the pixel polygon for drawing/highlighting a region.

        Args:
            r: The R enum value
            board_size: (width, height) of the board image

        Returns:
            List of (x, y) pixel coordinates, or None
        """
        region = self.regions_by_enum.get(r)
        if region is None:
            return None

        return region.get_pixel_polygon(board_size[0], board_size[1])
