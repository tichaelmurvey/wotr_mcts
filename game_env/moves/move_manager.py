from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from typing import TYPE_CHECKING, Any, Callable, List, Tuple
from game_env.moves.ACTION_OPTION_OBSERVERS import ACTION_OPTION_OBSERVERS
from game_env.moves.ACTION_RESOLVERS import ACTION_RESOLVERS
from game_env.moves.move_types import (
    ActionSpace,
    MoveOption,
    MoveOptionTree,
    OptionBranch,
    OptsPolicy,
)

if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from game_env.action_signal_types import ActionSignal
    from game_env.moves.card_moves import MoveOptionSet
    from game_env.moves.move_types import ActionChoice, ActionChoiceSet


class MoveManager:
    action_tree: MoveOptionTree | None

    def __init__(self, game_env: WotrGame):
        self.game_env = game_env
        self.action_ongoing = False
        self.action_tree = None

    def execute_player_action(self, action_choice: ActionChoice):
        if self.action_ongoing:
            pass
        for move in action_choice:
            ACTION_RESOLVERS[move.move_type](self.game_env, move.move_target)

    def generate_moves(
        self, action_signal: ActionSignal, policy: OptsPolicy = OptsPolicy.FLAT
    ):
        if not action_signal.action_type in ACTION_OPTION_OBSERVERS:
            raise Exception(
                "No action operator for move", action_signal.action_type.name
            )
        move_definition = ACTION_OPTION_OBSERVERS[action_signal.action_type](
            action_signal.move_data
        )
        if isinstance(move_definition, MoveOptionTree):
            self.action_ongoing = True
            self.action_tree = move_definition
            step_options: ActionChoiceSet = tuple(
                (branch.this_step_choice,) for branch in move_definition.option_branches
            )
            self.game_env.current_action_space = ActionSpace(step_options, 1)
        else:
            moves, num_moves = MoveManager._aggregate_options(move_definition)
            self.game_env.current_action_space = ActionSpace(moves, num_moves)

    @staticmethod
    def _aggregate_options(option_set: MoveOptionSet) -> Tuple[ActionChoiceSet, int]:
        if option_set.policy == OptsPolicy.FLAT and option_set.num_to_choose > 1:
            flat_options: ActionChoiceSet = tuple(
                combinations(option_set.options, option_set.num_to_choose)
            )
            return flat_options, 1
        else:
            return (
                tuple((action,) for action in option_set.options),
                option_set.num_to_choose,
            )


def flatten_tree(option_tree: MoveOptionTree) -> ActionChoiceSet:
    moves: List[List[MoveOption]] = []
    for next_branch in option_tree.option_branches:
        moves += flatten_branch(next_branch)
    action_choice_set = tuple(tuple(inner) for inner in moves)
    return action_choice_set


def flatten_branch(branch: OptionBranch) -> List[List[MoveOption]]:
    if branch.next_step_options is None:
        return [[branch.this_step_choice]]
    node_branches: List[List[MoveOption]] = []
    for next_branch in branch.next_step_options:
        node_branches += flatten_branch(next_branch)

    node_branches_with_head = [
        [branch.this_step_choice] + new_branch for new_branch in node_branches
    ]

    return node_branches_with_head
