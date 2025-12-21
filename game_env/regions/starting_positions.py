from collections import Counter, namedtuple
from typing import NamedTuple, Tuple

from game_env.army import AU, GenericUnitGroup, GenericUnitGroupWithNazgul
from game_env.regions_enum import R


class StartingPosition(NamedTuple):
    region_id: R
    units: GenericUnitGroupWithNazgul


STARTING_POSITIONS: Tuple[StartingPosition, ...] = (
    # Dwarves
    StartingPosition(
        R.EREBOR, Counter(Counter({AU.dwar_reg: 1, AU.dwar_elt: 2, AU.dwar_ldr: 1}))
    ),
    StartingPosition(R.ERED_LUIN, Counter(Counter({AU.dwar_reg: 1}))),
    StartingPosition(R.IRON_HILLS, Counter({AU.dwar_reg: 1})),
    # Elves
    StartingPosition(
        R.GREY_HAVENS, Counter({AU.elvn_reg: 1, AU.elvn_elt: 1, AU.elvn_ldr: 1})
    ),
    StartingPosition(R.RIVENDELL, Counter({AU.elvn_elt: 2, AU.elvn_ldr: 1})),
    StartingPosition(
        R.WOODLAND_REALM, Counter({AU.elvn_reg: 1, AU.elvn_elt: 1, AU.elvn_ldr: 1})
    ),
    StartingPosition(
        R.LORIEN, Counter({AU.elvn_reg: 1, AU.elvn_elt: 2, AU.elvn_ldr: 1})
    ),
    # AU.Gondor    StartingPosition(R.MINAS_TIRITH, Counter({AU.gond_reg: 3, AU.gond_elt: 1, AU.gond_ldr: 1})),
    StartingPosition(R.DOL_AMROTH, Counter({AU.gond_reg: 3})),
    StartingPosition(R.OSGILIATH, Counter({AU.gond_reg: 2})),
    StartingPosition(R.PELARGIR, Counter({AU.gond_reg: 1})),
    # The North
    StartingPosition(R.BREE, Counter({AU.nort_reg: 1})),
    StartingPosition(R.CARROCK, Counter({AU.nort_reg: 1})),
    StartingPosition(R.DALE, Counter({AU.nort_reg: 1, AU.nort_ldr: 1})),
    StartingPosition(R.NORTH_DOWNS, Counter({AU.nort_elt: 1})),
    StartingPosition(R.THE_SHIRE, Counter({AU.nort_reg: 1})),
    # Rohan
    StartingPosition(R.EDORAS, Counter({AU.rohn_reg: 1, AU.rohn_elt: 1})),
    StartingPosition(R.FORDS_OF_ISEN, Counter({AU.rohn_reg: 2, AU.rohn_ldr: 1})),
    StartingPosition(R.HELMS_DEEP, Counter({AU.rohn_reg: 1})),
    # Isengard
    StartingPosition(R.ORTHANC, Counter({AU.isen_reg: 4, AU.isen_elt: 1})),
    StartingPosition(R.NORTH_DUNLAND, Counter({AU.isen_reg: 1})),
    StartingPosition(R.SOUTH_DUNLAND, Counter({AU.isen_reg: 1})),
    # Sauron
    StartingPosition(
        R.BARAD_DUR, Counter({AU.mord_reg: 4, AU.mord_elt: 1, "nazgul": 1})
    ),
    StartingPosition(
        R.DOL_GULDUR, Counter({AU.mord_reg: 5, AU.mord_elt: 1, "nazgul": 1})
    ),
    StartingPosition(R.GORGOROTH, Counter({AU.mord_reg: 3})),
    StartingPosition(R.MINAS_MORGUL, Counter({AU.mord_reg: 5, "nazgul": 1})),
    StartingPosition(R.MORIA, Counter({AU.mord_reg: 2})),
    StartingPosition(R.MOUNT_GUNDABAD, Counter({AU.mord_reg: 2})),
    StartingPosition(R.NURN, Counter({AU.mord_reg: 2})),
    StartingPosition(R.MORANNON, Counter({AU.mord_reg: 5, "nazgul": 1})),
    # Southrons & Easterlings
    StartingPosition(R.FAR_HARAD, Counter({AU.east_reg: 3, AU.east_elt: 1})),
    StartingPosition(R.NEAR_HARAD, Counter({AU.east_reg: 3, AU.east_elt: 1})),
    StartingPosition(R.NORTH_RHUN, Counter({AU.east_reg: 2})),
    StartingPosition(R.SOUTH_RHUN, Counter({AU.east_reg: 3, AU.east_elt: 1})),
    StartingPosition(R.UMBAR, Counter({AU.east_reg: 3})),
)

REINFORCEMENTS_FREE = Counter(
    {
        AU.dwar_reg: 2,
        AU.dwar_elt: 3,
        AU.dwar_ldr: 3,
        AU.elvn_reg: 2,
        AU.elvn_elt: 4,
        AU.gond_reg: 6,
        AU.gond_elt: 4,
        AU.gond_ldr: 3,
        AU.nort_reg: 6,
        AU.nort_elt: 4,
        AU.nort_ldr: 3,
        AU.rohn_reg: 6,
        AU.rohn_elt: 4,
        AU.rohn_ldr: 3,
    }
)

REINFORCEMENTS_SHADOW = Counter(
    {
        AU.isen_reg: 6,
        AU.isen_elt: 5,
        AU.mord_reg: 8,
        AU.mord_elt: 4,
        "nazgul": 4,
        AU.east_reg: 10,
        AU.east_elt: 3,
    }
)
