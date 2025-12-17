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

from game_env.moves import card_moves
from game_env.moves import fellowship_moves

ACTION_OPTION_OBSERVERS: dict[MT, OptionsFn] = {
    MT.EVENT_CARD_DISCARD: card_moves.define_options,
    MT.CHANGE_GUIDE: fellowship_moves.define_options_guide,
    MT.DECLARE_FELLOWSHIP: fellowship_moves.define_options_declare,
    MT.HUNT_ALLOCATION: fellowship_moves.define_options_hunt_allocation
}

ACTION_RESOLVERS : dict[MT, ExecuteFn] = {
    MT.EVENT_CARD_DISCARD : card_moves.execute_action,
    MT.CHANGE_GUIDE: fellowship_moves.execute_action_guide,
    MT.DECLARE_FELLOWSHIP: fellowship_moves.execute_action_declare,
    MT.HUNT_ALLOCATION: fellowship_moves.execute_action_hunt_allocation
}

"""
==== Action management heirarchy summary ====

A "Move" is one player-initiated change to the game state.

An "Action" is a set of 1 or more moves, between which there is no random event or opponent action (e.g. discard 2 cards)

When the game state progresses to a point which requires a player action, this action requirement is logged in action_triage.
For example, there may be a triaged action for each action die during the action phase.

Each triaged action is resolved by the movesgenerator into possible moves or movesets. 
Then, moveset options are provided to the player in the form of an ActionSpace. 
The player chooses an action and returns it through implement_player_action.
The env then executes each move in the action by indexing the move type to move execution functions.
"""
class MovesGenerator:
    @staticmethod
    def generate_moves(action_signal: ActionSignal):
        if not action_signal.action_type in ACTION_OPTION_OBSERVERS:
            raise Exception("No action operator for move", action_signal.action_type.name)
        moves, num_moves = MovesGenerator._aggregate_options(                
            ACTION_OPTION_OBSERVERS[action_signal.action_type](
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