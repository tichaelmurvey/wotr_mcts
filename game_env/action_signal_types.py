from __future__ import annotations
from typing import List
from game_env.game_env_enums import Player
from game_env.moves.move_types import CardList, MoveType


from dataclasses import dataclass


@dataclass
class ActionSignal:
    action_type: MoveType
    action_player: Player | None = None
    move_data: None | CardList = None


S = ActionSignal
ActionRequirement = List[ActionSignal]

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