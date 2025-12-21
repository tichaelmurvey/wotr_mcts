from typing import Tuple

from game_env.action_dice.dice import A, ActionDie, ActionResult


DiceSet = Tuple[ActionDie, ...]


class DicePool:
    action_dice: DiceSet

    def __init__(self, Die: type[ActionDie], n: int = 0):
        self.action_dice = tuple(Die() for _ in range(n))

    def action_roll(self):
        for die in self.action_dice:
            if die.action_used:
                continue
            die.roll()

    def get_unused_die_results(self):
        return [die.current_result for die in self.action_dice if not die.action_used]

    def get_dice_results(self):
        return [die.current_result for die in self.action_dice]

    def recover_dice(self):
        # TODO: Set all dice to used = false
        pass

    def get_non_available_sides(self) -> list[ActionResult]:
        conversion_options: list[ActionResult] = []
        active_results = self.get_unused_die_results()
        for side in self.action_dice[0].sides:
            if side in active_results:
                continue
            if side is A.WILL:
                continue
            conversion_options.append(side)
        return conversion_options

    def is_ring_useful(self) -> bool:
        return len(self.get_non_available_sides()) is not 0
