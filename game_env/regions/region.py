from collections import Counter
from enum import IntEnum
from typing import Tuple

from game_env.army import Army, UnitGroup
from game_env.characters import CompanionName, MinionName
from game_env.game_env_enums import Nation, get_nation_player
from game_env.regions_enum import R


class RegionFeature(IntEnum):
    TOWN = 0
    CITY = 1
    STRONGHOLD = 2
    FORT = 3
    COASTAL = 4
    EASTERN = 5
RF = RegionFeature

class RegionBase:
    units: UnitGroup

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
        idx: R,
        name: str,
        adj_regions: set[R],
        nation: Nation | None = None,
        features: set[RegionFeature] | None = None,
    ):
        self.occupied = False
        self.idx = idx
        self.name = name
        self.nation = nation
        self.adj_regions = adj_regions
        self.features = features
        self.has_settlement = (
            True if features and features & {RF.STRONGHOLD, RF.CITY, RF.TOWN} else False
        )
        self.control = (
            get_nation_player(nation) if self.has_settlement and nation else None
        )
        super().__init__()

    def set_starting_units(self, units: UnitGroup):
        self.units = units

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
