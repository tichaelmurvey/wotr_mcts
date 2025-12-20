from collections import Counter
from itertools import product
from typing import List

from game_env.army import Army, ArmyUnit, GenericUnitGroup
from game_env.moves.move_types import (
    MT,
    ActionChoiceSet,
    MoveOption,
    MoveOptionTree,
    OptionBranch,
)

units: GenericUnitGroup = Counter(
    {
        ArmyUnit.nort_elt: 3,
        ArmyUnit.dwar_elt: 2,
        ArmyUnit.dwar_ldr: 2,
    }
)


def counter_combinations(counter: Counter) -> list[dict]:
    """
    Generate all unique combinations of elements up to their counts.
    """

    keys = list(counter.keys())
    ranges = [range(counter[k] + 1) for k in keys]

    return [dict(zip(keys, counts)) for counts in product(*ranges)]


combos = counter_combinations(units)
for combo in combos:
    print(combo)
print(len(combos))
