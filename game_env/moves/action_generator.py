from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from typing import TYPE_CHECKING, Any, Callable, List, Tuple
from game_env.moves.move_types import MT, ActionSpace,OptsPolicy

if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from game_env.action_signal_types import ActionSignal
    from game_env.moves.card_moves import MoveOptionSet
    from game_env.moves.move_types import (
        ActionChoice,
        ActionChoiceSet
    )

type OptionsFn = Callable[[Any], MoveOptionSet]
type ExecuteFn = Callable[[WotrGame, Any]]

@dataclass
class ActionOperator:
    define_options: OptionsFn
    execute_action: ExecuteFn

from game_env.moves.card_moves import discard_operator
ACTION_OPERATORS: List[ActionOperator] = []
ACTION_OPERATORS.insert(MT.EVENT_CARD_DISCARD, discard_operator)


class MovesGenerator:
    @staticmethod
    def generate_moves(action_signal: ActionSignal):
        if not action_signal.action_type in ACTION_OPERATORS:
            raise Exception("No action operator for move", action_signal.action_type.name)
        moves, num_moves = MovesGenerator._aggregate_options(                
            ACTION_OPERATORS[action_signal.action_type].define_options(
                action_signal.move_data
            )
        )
        return ActionSpace(moves, num_moves)

    @staticmethod
    def _aggregate_options(option_set: MoveOptionSet) -> Tuple[ActionChoiceSet, int]:
        if option_set.policy == OptsPolicy.FLAT and option_set.num > 1:
            flat_options: ActionChoiceSet = tuple(
                combinations(option_set.options, option_set.num)
            )
            return flat_options, 1
        else:
            return tuple((action,) for action in option_set.options), option_set.num


class ActionResolver:
    def __init__(self, game_env: WotrGame):
        self.game_env = game_env

    def resolve_action(self, action_choice: ActionChoice):
        for action in action_choice:
            ACTION_OPERATORS[action.move_type].execute_action(
                self.game_env, action.move_target
            )
