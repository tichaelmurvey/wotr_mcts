from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from game_env.action_signal_types import S
from game_env.game_env_enums import (
    P,
    TCT,
)
from game_env.hunt.hunt_pool import HuntPool
from game_env.hunt.hunt_tiles import HuntTile

from game_env.moves.action_generator import MT

@dataclass
class HuntBox:
    fp_dice = 0
    eyes = 0


class HuntPhase(IntEnum):
    BEFORE_HUNT_ROLL = -1
    HUNT_ROLL = 0
    TILE_DRAW_IMMINENT = 1
    DRAW_TILE = 2
    DAMAGE_SOAK_CARD = 3
    GUIDE_ABILITY = 4
    USE_ONE_RING = 5
    RESOLVE_REVEAL = 6
    HUNT_COMPLETE = 7


HP = HuntPhase


class Hunt:
    active_tile: HuntTile | None
    pool: HuntPool
    phase: HuntPhase

    def __init__(self, game_env: WotrGame):
        self.game_env = game_env
        self.pool = game_env.hunt_pool
        self.box = game_env.hunt_box
        self.in_mordor = game_env.fellowship.in_mordor
        self.trigger = self.game_env.check_table_triggers
        self.phase = HP.TILE_DRAW_IMMINENT if self.in_mordor else HP.BEFORE_HUNT_ROLL
        self.active_tile = None
        self.hits = 0
        self.active_tile_damage = 0

    def progress_hunt(self):
        match self.phase:

            case HP.HUNT_ROLL:
                self.hunt_roll()
            case HP.TILE_DRAW_IMMINENT:
                self.tile_draw_imminent()
            case HP.DRAW_TILE:
                self.draw_tile()
            case HP.DAMAGE_SOAK_CARD:
                self.check_card_soak()
            case HP.GUIDE_ABILITY:
                self.check_guide_ability()
            case HP.USE_ONE_RING:
                self.use_one_ring()
            case HP.RESOLVE_REVEAL:
                self.resolve_reveal()
            case HP.HUNT_COMPLETE:
                return

        if len(self.game_env.action_triage) == 0:
            self.nxtphase()
            self.progress_hunt()

    def nxtphase(self):
        self.phase = HuntPhase(self.phase + 1)

    def before_hunt_roll(self):
        self.trigger(TCT.BEFORE_HUNT_ROLL, MT.USE_HUNT_TABLE_CARD)

    def hunt_roll(self):
        dice = self.box.eyes
        target = 6 - self.box.fp_dice
        rerolls = self.calc_rerolls()
        hits = sum(random.randint(1, 6) >= target for _ in range(dice))
        hits += sum(
            random.randint(1, 6) >= target for _ in range(min(rerolls, dice - hits))
        )
        self.hits = hits

    def tile_draw_imminent(self):
        self.trigger(TCT.HUNT_SUCCESS, MT.USE_HUNT_TABLE_CARD)

    def draw_tile(self):
        self.active_tile = self.pool.draw_tile()
        self.trigger(TCT.HUNT_TILE_DRAWN, MT.USE_HUNT_TABLE_CARD)

    def check_card_soak(self):
        self.calc_hunt_damage()
        self.trigger(TCT.HUNT_DAMAGE, MT.USE_HUNT_TABLE_CARD)

    def check_guide_ability(self):
        if self.active_tile_damage > 0:
            self.game_env.action_triage.append(S(MT.USE_GUIDE_HUNT_ABILITY))

    def use_one_ring(self):
        self.game_env.fellowship.add_corruption(self.active_tile_damage)

    def resolve_reveal(self):
        if self.active_tile.reveal:  # type: ignore
            self.game_env.fellowship.reveal()

    def calc_hunt_damage(self):
        if self.active_tile is None:
            return
        tile = self.active_tile
        if not tile.eye and not tile.special_action:
            self.active_tile_damage = tile.damage
        elif tile.eye and self.in_mordor:
            self.active_tile_damage = self.box.eyes + self.box.fp_dice
        elif tile.eye and not self.in_mordor:
            self.active_tile_damage = self.hits
        elif tile.special and tile.special_action is "shelob":
            self.active_tile_damage = random.randint(1, 6)

    def calc_rerolls(self):
        region = self.game_env.fellowship.region
        rerolls = 0
        if region.get_num_nazgul() > 0:
            rerolls += 1
        if region.army and region.army.player is P.SHADOW:
            rerolls += 1
        if (
            region.features
            and "stronghold" in region.features
            and region.control is P.SHADOW
        ):
            rerolls += 1
        return rerolls
