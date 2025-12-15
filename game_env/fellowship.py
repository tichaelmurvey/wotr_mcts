from __future__ import annotations
from copy import copy
from typing import Tuple
from game_env.characters import C
from game_env.action_signal_types import ActionSignal
from game_env.action_signal_types import ActionRequirement
from game_env.characters import COMPANION_NAMES
from game_env.game_env_enums import P
from game_env.moves.action_generator import MT
from game_env.regions.region import Region
from game_env.regions_enum import R


class Fellowship:
    def __init__(self, action_triage: ActionRequirement, regions: Tuple[Region, ...]):
        self.action_triage = action_triage
        self.regions = regions
        self.companions = copy(COMPANION_NAMES)
        self.track_position = 0
        self.region = regions[R.RIVENDELL]
        self.corruption = 0
        self.guide = C.GANDALF_GREY
        self.revealed = False
        self.in_mordor = False
        self.mordor_step = None

    def move(self):
        pass

    def reveal(self):
        pass

    def declare(self):
        pass

    def change_guide(self):
        pass

    def add_corruption(self, corruption: int):
        pass

    def fellowship_phase(self):
        self.action_triage.append(ActionSignal(MT.DECLARE_FELLOWSHIP, P.FREE))
        self.action_triage.append(ActionSignal(MT.CHANGE_GUIDE, P.FREE))
