from __future__ import annotations
from collections import Counter
from enum import IntEnum
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from game_env.army import GenericUnitGroup
    from game_env.characters import CompanionName, MinionName
    from game_env.game_env_enums import P, Nation
    from game_env.regions_enum import R
    from game_env.game_env import WotrGame

from game_env.game_env_enums import get_nation_player
from game_env.army import Army

class RegionFeature(IntEnum):
    TOWN = 0
    CITY = 1
    STRONGHOLD = 2
    FORT = 3
    COASTAL = 4
    EASTERN = 5
RF = RegionFeature

class RegionBase:
    units: GenericUnitGroup

    def __init__(self):
        self.units = Counter()
        self.companions: set[CompanionName] = set()
        self.minions: set[MinionName] = set()
        self.nazgul: int = 0
        self.army: Army | None = None

    def get_num_nazgul(self) -> int:
        return self.nazgul + (1 if "wking" in self.minions else 0) #TODO: Update this for enum

    def update_army(self):
        if not self.units:
            self.army = None
        else:
            self.army = Army(self.units, self.minions, self.companions, self.nazgul)


class Region(RegionBase):
    def __init__(
        self,
        game_env: WotrGame,
        idx: R,
        name: str,
        adj_regions: set[R],
        nation: Nation | None = None,
        features: set[RegionFeature] | None = None,
    ):
        self.game_env = game_env
        self.idx = idx
        self.name = name
        self.nation = nation
        self.orig_loyalty = get_nation_player(nation) if self.has_settlement and nation else None
        self.adj_regions = adj_regions
        self.features = features
        self.has_settlement = True if features and features & {RF.STRONGHOLD, RF.CITY, RF.TOWN} else False
        self.city_or_stronghold = True if features and features & {RF.STRONGHOLD, RF.CITY} else False
        self.control = self.orig_loyalty
        super().__init__()

    def set_starting_units(self, units: GenericUnitGroup):
        self.units = units

    def can_muster_action(self, player : P):
        if not self.has_settlement or not self.nation:
            return False

        if self.orig_loyalty is not player:
            return False
        
        if self.control is not player:
            return False
        
        if not self.game_env.politics.nations[self.nation].at_war:
            return False
        
        return True
        


def get_n_regions_away(region_id: R, n_steps: int, regions: Tuple[Region, ...]) -> Tuple[R, ...]:
    current_region = regions[region_id]
    if n_steps == 0:
        return (region_id,)
    
    adj_regions = tuple(region_id for region_id in current_region.adj_regions)
    if n_steps == 1:
        return adj_regions
    else:
        return tuple(region for adj in adj_regions for region in get_n_regions_away(adj, n_steps-1, regions))

class SeigeRegion(RegionBase):
    def __init__(self):
        super().__init__()
