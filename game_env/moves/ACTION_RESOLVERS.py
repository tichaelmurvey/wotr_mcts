from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_env.moves.move_types import MT, ExecuteFn

from game_env.moves import card_moves, fellowship_moves, resolve_action_die

ACTION_RESOLVERS: dict[MT, ExecuteFn] = {
    MT.EVENT_CARD_DISCARD: card_moves.execute_action,
    MT.CHANGE_GUIDE: fellowship_moves.execute_action_guide,
    MT.DECLARE_FELLOWSHIP: fellowship_moves.execute_action_declare,
    MT.HUNT_ALLOCATION: fellowship_moves.execute_action_hunt_allocation,
    MT.RESOLVE_ACTION_DIE: resolve_action_die.execute_resolve_die,
    # Die action executors
    MT.MOVE_ARMY: resolve_action_die.execute_move_army,
    MT.ATTACK: resolve_action_die.execute_attack,
    MT.MUSTER: resolve_action_die.execute_muster,
    MT.ADVANCE_NATION_POLITICS: resolve_action_die.execute_advance_politics,
    MT.MOVE_FELLOWSHIP: resolve_action_die.execute_fellowship_move,
    MT.HIDE_FELLOWSHIP: resolve_action_die.execute_hide_fellowship,
    MT.DRAW_CARD: resolve_action_die.execute_draw_card,
    MT.PASS: resolve_action_die.execute_pass,
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

Type heirarchy:

- MoveOption: One game state change. Contains type, and targeting data, e.g. MOVE_ARMY, (region_from, region_to)
Part of both move offering and move response

- MoveOptionSet: Intermediate step in flat, independent offering defintion
Contains MoveOptions, how many options to pick, and policy for how options should be presented (flat, or in tree) Can contain multiple independent player decisions, e.g. discard 2 cards but not dependent decisions e.g. which card to play -> which units to muster

- ActionChoice: Tuple of MoveOptions.
Used in offering as one decision space, possibly among several.
Player decision responses are of this type, to be executed in order.

- ActionChoiceSet: Tuple of MoveOptions.
Used to offer player a set of action decisions.

- ActionTree: Recursive tree of action options, with some shared properties.

- OptionBranch: One top level option, and its possible children, and any outcome calcs they can share

=== FLAT POLICY ACTION SPACE ===
ActionSpace
    num_moves = 1
    ActionChoiceSet
        Combos x ActionChoice - where combos is options ^ choices_needed. These are the action options, complete from start to end of the action space, one is picked
            choices_needed x MoveOption - where steps is how many individual moves are made before a random or other player action.

=== INDEPENDENT SEQUENTIAL POLICY ACTION SPACE ===
ActionSpace
    num_moves = choices_needed - where choices_needed is how many of the provided options should be picked
    ActionChoiceSet
        options x ActionChoice
            1 x MoveOption - Generally, could be 2 if they are packaged together for convenience of env reading, but zero meaningful decision making between them if so.

=== DEPENDENT SEQUENTIAL POLICY ACTION SPACE ===
ActionTree
    shared_state - dict of data needed in many possible branches, e.g. legal army movements
    step_options x OptionBranch where step_options is the options for this step, e.g. choose action die options might be 4
        ActionChoice - one option at this branch. Note some flattening can still be used here, e.g. for resolving 2 army movements.
        step_options x OptionBranch, or None if this is step ends the move.

Why do this bespoke move tracking, rather than using game_env updates? 
Because you might want to have two players engaging with the same env under different move policies. 
For example, the human-usable GUI needs most options very flat - you don't want to be making gamestate updates every time the player selects a die to "preview" actions. But you might be playing against a model that needs sequential steps to be smart.
The advantage of this approach is you avoid conditionally appending more actions to the move triage in lots of move executions. Also, you keep conceptual clarity and separate management of "Action" and "Move".
"""
