from typing import Tuple

from game_env.action_dice.dice import ActionDie


DiceSet = Tuple[ActionDie, ...]


class DicePool:
    action_dice: DiceSet

    def __init__(self, Die: type[ActionDie], n: int = 0):
        self.action_dice = tuple(Die() for _ in range(n))

    def roll_dice(self):
        for die in self.action_dice:
            die.roll()

    def get_dice_results(self):
        return [die.current_result for die in self.action_dice]

    def recover_dice(self):
        # TODO: Set all dice to used = false
        pass
