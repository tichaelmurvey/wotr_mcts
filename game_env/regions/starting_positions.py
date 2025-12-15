from collections import Counter, namedtuple
from typing import NamedTuple, Tuple, TypedDict

from game_env.army import FU, SU, UnitGroup
from game_env.regions_enum import R


class StartingPosition(NamedTuple):
    region_id: R
    units: UnitGroup


STARTING_POSITIONS: Tuple[StartingPosition, ...] = (
    # Dwarves
    StartingPosition(
        R.EREBOR, Counter(Counter({FU.dwar_reg: 1, FU.dwar_elt: 2, FU.dwar_ldr: 1}))
    ),
    StartingPosition(R.ERED_LUIN, Counter(Counter({FU.dwar_reg: 1}))),
    StartingPosition(R.IRON_HILLS, Counter({FU.dwar_reg: 1})),
    # Elves
    StartingPosition(
        R.GREY_HAVENS, Counter({FU.elvn_reg: 1, FU.elvn_elt: 1, FU.elvn_ldr: 1})
    ),
    StartingPosition(R.RIVENDELL, Counter({FU.elvn_elt: 2, FU.elvn_ldr: 1})),
    StartingPosition(
        R.WOODLAND_REALM, Counter({FU.elvn_reg: 1, FU.elvn_elt: 1, FU.elvn_ldr: 1})
    ),
    StartingPosition(
        R.LORIEN, Counter({FU.elvn_reg: 1, FU.elvn_elt: 2, FU.elvn_ldr: 1})
    ),
    # FU.Gondor    StartingPosition(R.MINAS_TIRITH, Counter({FU.gond_reg: 3, FU.gond_elt: 1, FU.gond_ldr: 1})),
    StartingPosition(R.DOL_AMROTH, Counter({FU.gond_reg: 3})),
    StartingPosition(R.OSGILIATH, Counter({FU.gond_reg: 2})),
    StartingPosition(R.PELARGIR, Counter({FU.gond_reg: 1})),
    # The North
    StartingPosition(R.BREE, Counter({FU.nort_reg: 1})),
    StartingPosition(R.CARROCK, Counter({FU.nort_reg: 1})),
    StartingPosition(R.DALE, Counter({FU.nort_reg: 1, FU.nort_ldr: 1})),
    StartingPosition(R.NORTH_DOWNS, Counter({FU.nort_elt: 1})),
    StartingPosition(R.THE_SHIRE, Counter({FU.nort_reg: 1})),
    # Rohan
    StartingPosition(R.EDORAS, Counter({FU.rohn_reg: 1, FU.rohn_elt: 1})),
    StartingPosition(R.FORDS_OF_ISEN, Counter({FU.rohn_reg: 2, FU.rohn_ldr: 1})),
    StartingPosition(R.HELMS_DEEP, Counter({FU.rohn_reg: 1})),
    # Isengard
    StartingPosition(R.ORTHANC, Counter({SU.isen_reg: 4, SU.isen_elt: 1})),
    StartingPosition(R.NORTH_DUNLAND, Counter({SU.isen_reg: 1})),
    StartingPosition(R.SOUTH_DUNLAND, Counter({SU.isen_reg: 1})),
    # Sauron
    StartingPosition(
        R.BARAD_DUR, Counter({SU.mord_reg: 4, SU.mord_elt: 1, SU.nazgul: 1})
    ),
    StartingPosition(
        R.DOL_GULDUR, Counter({SU.mord_reg: 5, SU.mord_elt: 1, SU.nazgul: 1})
    ),
    StartingPosition(R.GORGOROTH, Counter({SU.mord_reg: 3})),
    StartingPosition(R.MINAS_MORGUL, Counter({SU.mord_reg: 5, SU.nazgul: 1})),
    StartingPosition(R.MORIA, Counter({SU.mord_reg: 2})),
    StartingPosition(R.MOUNT_GUNDABAD, Counter({SU.mord_reg: 2})),
    StartingPosition(R.NURN, Counter({SU.mord_reg: 2})),
    StartingPosition(R.MORANNON, Counter({SU.mord_reg: 5, SU.nazgul: 1})),
    # Southrons & Easterlings
    StartingPosition(R.FAR_HARAD, Counter({SU.east_reg: 3, SU.east_elt: 1})),
    StartingPosition(R.NEAR_HARAD, Counter({SU.east_reg: 3, SU.east_elt: 1})),
    StartingPosition(R.NORTH_RHUN, Counter({SU.east_reg: 2})),
    StartingPosition(R.SOUTH_RHUN, Counter({SU.east_reg: 3, SU.east_elt: 1})),
    StartingPosition(R.UMBAR, Counter({SU.east_reg: 3})),
)

REINFORCEMENTS_FREE = Counter(
    {
        FU.dwar_reg: 2,
        FU.dwar_elt: 3,
        FU.dwar_ldr: 3,
        FU.elvn_reg: 2,
        FU.elvn_elt: 4,
        FU.gond_reg: 6,
        FU.gond_elt: 4,
        FU.gond_ldr: 3,
        FU.nort_reg: 6,
        FU.nort_elt: 4,
        FU.nort_ldr: 3,
        FU.rohn_reg: 6,
        FU.rohn_elt: 4,
        FU.rohn_ldr: 3,
    }
)

REINFORCEMENTS_SHADOW = Counter(
    {
        SU.isen_reg: 6,
        SU.isen_elt: 5,
        SU.mord_reg: 8,
        SU.mord_elt: 4,
        SU.nazgul: 4,
        SU.east_reg: 10,
        SU.east_elt: 3,
    }
)
