from collections import Counter
from enum import IntEnum

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


class RegionBase:
    units: UnitGroup

    def __init__(self):
        self.units = Counter()
        self.companions: set[CompanionName] = set()
        self.minions: set[MinionName] = set()
        self.nazgul: int = 0
        self.army: Army | None = None

    def get_num_nazgul(self) -> int:
        return self.nazgul + (1 if "wking" in self.minions else 0)

    def update_army(self):
        if not self.units:
            self.army = None
        else:
            self.army = Army(self.units, self.minions, self.companions, self.nazgul)


class Region(RegionBase):
    def __init__(
        self,
        idx: int,
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
            True if features and features & {"stronghold", "city", "town"} else False
        )
        self.control = (
            get_nation_player(nation) if self.has_settlement and nation else None
        )
        super().__init__()

    def set_starting_units(self, units: UnitGroup):
        self.units = units


class SeigeRegion(RegionBase):
    def __init__(self):
        super().__init__()
