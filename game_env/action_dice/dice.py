from enum import IntEnum
import random
from typing import Tuple


class ActionResult(IntEnum):
    CHARACTER = 0
    MUSTER = 1
    PALANTIR = 2
    ARMY = 3
    HYBRID = 4
    WILL = 5
    EYE = 6


A = ActionResult

DieSides = Tuple[A, A, A, A, A, A]


class ActionDie:
    sides: DieSides

    def __init__(self):
        self.current_result: ActionResult = ActionResult.CHARACTER
        self.action_used = False

    def roll(self):
        self.current_result = random.choice(self.sides)

    def use_die(self):
        self.action_used = True


class ActionDieFree(ActionDie):
    def __init__(self):
        self.sides: DieSides = (
            A.WILL,
            A.CHARACTER,
            A.CHARACTER,
            A.HYBRID,
            A.MUSTER,
            A.PALANTIR,
        )
        super().__init__()


class ActionDieShadow(ActionDie):
    def __init__(self):
        self.sides: DieSides = (
            A.EYE,
            A.CHARACTER,
            A.ARMY,
            A.HYBRID,
            A.MUSTER,
            A.PALANTIR,
        )
        super().__init__()
