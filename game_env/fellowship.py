from __future__ import annotations
from copy import copy
from typing import Tuple
from game_env.characters import C, CompanionName
from game_env.action_signal_types import ActionSignal
from game_env.action_signal_types import ActionRequirement
from game_env.characters import COMPANION_NAMES
from game_env.game_env_enums import P
from game_env.moves.action_generator import MT
from game_env.regions.region import RF, Region
from game_env.regions_enum import R


class Fellowship:
    region : Region
    companions : Tuple[CompanionName, ...]
    moved_last_turn: bool
    moved_this_turn : bool
    def __init__(self, action_triage: ActionRequirement, regions: Tuple[Region, ...]):
        self.action_triage = action_triage
        self.regions = regions
        self.moved_last_turn = False
        self.moved_this_turn = False
        self.companions = (
            C.STRIDER,
            C.GANDALF_GREY,
            C.BOROMIR,
            C.LEGOLAS,
            C.GIMLI,
            C.MERRY,
            C.PIPPIN
        )
        self.track_position = 0
        self.region = regions[R.RIVENDELL]
        self.corruption = 0
        self.guide = C.GANDALF_GREY
        self.revealed = False
        self.in_mordor = False
        self.mordor_step = None

    def move(self):
        self.moved_this_turn = True

    def reveal(self):
        pass

    def declare(self, region: R):
        self.track_position = 0
        self.region = self.regions[region]
        region_obj = self.regions[region]
        if region_obj.features and RF.STRONGHOLD in region_obj.features and region_obj.control==P.FREE and not region_obj.occupied:
            self.corruption = max(0, self.corruption-1)

    def change_guide(self, new_guide: CompanionName):
        self.guide = new_guide

    def add_corruption(self, corruption: int):
        pass

    def fellowship_phase(self):
        self.moved_last_turn = self.moved_this_turn
        self.moved_this_turn = False

        if not self.revealed and not self.in_mordor:
            self.action_triage.append(ActionSignal(MT.DECLARE_FELLOWSHIP, P.FREE, self))
        self.action_triage.append(ActionSignal(MT.CHANGE_GUIDE, P.FREE, self))
