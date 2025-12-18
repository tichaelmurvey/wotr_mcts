from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple

from game_env.game_env_enums import N, Nation, P, Player, get_nation_player
from game_env.action_dice.dice import ActionResult, A
from game_env.characters import CHARACTER_STATS, C, M, CompanionName, MinionName
from game_env.moves.define_attack_options import define_attack_options
from game_env.moves.define_half_move_options import define_half_move_options
from game_env.moves.define_muster_options import define_muster_options
from game_env.moves.move_types import (
    MT,
    MO,
    MoveOption,
    MoveOptionSet,
    ActionChoice,
    ActionChoiceSet,
    ActionSpace,
    OptsPolicy,
)
from game_env.regions.region import RF, RegionFeature

if TYPE_CHECKING:
    from game_env.fellowship import Fellowship
    from game_env.regions_enum import R
    from game_env.game_env import WotrGame
    from game_env.army import GenericUnitGroup
    from game_env.politics.politics import Politics


# ============================================================================
# CONSTANTS AND HELPERS
# ============================================================================

# Map action results to which actions they can perform
FP_DIE_ACTIONS: Dict[ActionResult, List[MT]] = {
    A.CHARACTER: [
        MT.MOVE_ARMY,
        MT.ATTACK,
        MT.MOVE_FELLOWSHIP,
        MT.HIDE_FELLOWSHIP,
        MT.MOVE_COMPANIONS,
        MT.SEPARATE_COMPANIONS,
        MT.PLAY_CARD,
    ],  # Army with leader only
    A.MUSTER: [
        MT.ADVANCE_NATION_POLITICS,
        MT.MUSTER,
        MT.PLAY_CARD,
    ],
    A.PALANTIR: [MT.DRAW_CARD, MT.PLAY_CARD],
    A.HYBRID: [  # Muster OR Army
        MT.MOVE_ARMY,
        MT.ATTACK,
        MT.ADVANCE_NATION_POLITICS,
        MT.MUSTER,
        MT.PLAY_CARD,
    ],
    A.WILL: [
        # Can convert to any other result
        MT.CONVERT_FROM_WOTW,
        # Can also recruit Aragorn or Gandalf White
        MT.RECRUIT_DICE_COMPANION,
    ],
}

SHADOW_DIE_ACTIONS: Dict[ActionResult, List[MT]] = {
    A.CHARACTER: [MT.MOVE_ARMY, MT.PLAY_CARD, MT.MOVE_MINIONS],  # Army with leader only
    A.ARMY: [MT.MOVE_ARMY, MT.ATTACK, MT.PLAY_CARD],
    A.MUSTER: [
        MT.ADVANCE_NATION_POLITICS,
        MT.MUSTER,
        MT.PLAY_CARD,
        # Shadow-specific:
        MT.RECRUIT_MINION,
    ],
    A.PALANTIR: [MT.DRAW_CARD, MT.PLAY_CARD],
    A.HYBRID: [  # Muster OR Army
        MT.MOVE_ARMY,
        MT.ATTACK,
        MT.ADVANCE_NATION_POLITICS,
        MT.MUSTER,
        MT.PLAY_CARD,
        MT.MOVE_MINIONS,
        MT.RECRUIT_MINION,
    ],
    A.EYE: [],  # Must go to hunt box, no actions
}

# Nations and their settlement regions (for mustering)
FREE_NATIONS = [N.NORTH, N.ELVES, N.DWARVES, N.ROHAN, N.GONDOR]
SHADOW_NATIONS = [N.ISENGARD, N.MORDOR, N.ELINGS]


def generate_diplomacy_options(
    game: WotrGame,
    player: Player,
) -> List[ActionChoice]:
    """
    Generate diplomatic action options (advancing nations on political track).

    Free Peoples: Can advance any FP nation, but "At War" only if nation is Active
    Shadow: Can advance any Shadow nation
    """
    options: List[ActionChoice] = []
    politics = getattr(game, "politics", None)
    if not politics:
        return options

    nations = FREE_NATIONS if player == P.FREE else SHADOW_NATIONS

    for nation in nations:
        status = politics.nations[nation]

        # Can't advance if already at war (position 3)
        if status.at_war:
            continue

        # Free Peoples: Can reach "At War" only if Active
        if player == P.FREE and status.track_pos == 2 and not status.active:
            continue

        move = MO(MT.ADVANCE_NATION_POLITICS, nation)
        options.append((move,))

    return options


def generate_fellowship_move_options(
    game: WotrGame,
) -> List[ActionChoice]:
    """Generate options to move the fellowship one step."""
    options: List[ActionChoice] = []

    fellowship = game.fellowship
    if fellowship.in_mordor:
        # Different movement rules in Mordor
        move = MO(MT.MOVE_FELLOWSHIP, None)
        options.append((move,))
    else:
        # Fellowship moves one step forward
        move = MO(MT.MOVE_FELLOWSHIP, None)
        options.append((move,))

    return options


def generate_hide_fellowship_options(
    game: WotrGame,
) -> List[ActionChoice]:
    """Generate option to hide a revealed fellowship."""
    options: List[ActionChoice] = []

    fellowship = game.fellowship
    if fellowship.revealed and not fellowship.in_mordor:
        move = MO(MT.HIDE_FELLOWSHIP, None)
        options.append((move,))

    return options


def generate_separate_companions_options(
    game: WotrGame,
) -> List[ActionChoice]:
    """
    Generate options to separate companions from the fellowship.

    Companions can move up to (fellowship_track_position + highest_companion_level) regions.
    """
    options: List[ActionChoice] = []

    fellowship = game.fellowship
    if not fellowship.companions:
        return options

    # Each companion or group can be separated
    for companion in fellowship.companions:
        move = MO(MT.SEPARATE_COMPANIONS, companion)
        options.append((move,))

    return options


def generate_move_companions_options(
    game: WotrGame,
) -> List[ActionChoice]:
    """
    Generate options to move companions on the map.

    Each companion/group moves up to their level in regions.
    """
    options: List[ActionChoice] = []

    # Find companions on the map (not in fellowship)
    for region in game.regions:
        if region.companions:
            for companion in region.companions:
                level = CHARACTER_STATS[companion].level
                # Generate destination options based on level
                # Simplified: just indicate the companion can move
                move = MO(MT.MOVE_COMPANIONS, (region.idx, companion))
                options.append((move,))

    return options


def generate_move_minions_options(
    game: WotrGame,
) -> List[ActionChoice]:
    """
    Generate options to move Shadow minions.

    Nazgûl can fly anywhere except into FP-controlled strongholds (unless besieging).
    Other minions move based on their level.
    """
    options: List[ActionChoice] = []

    # Move all Nazgûl to any valid region
    for region in game.regions:
        # Check if valid destination for Nazgûl
        if region.features and RF.STRONGHOLD in region.features:
            if region.control == P.FREE:
                # Can only enter if Shadow is besieging
                # Simplified: skip for now
                continue

        move = MO(MT.MOVE_MINIONS, ("nazgul", region.idx))
        options.append((move,))

    # Move other minions based on their position and level
    for minion, pos in game.minion_pos.items():
        if pos is not None:
            level = int(CHARACTER_STATS[minion].level)
            # Would need to calculate reachable regions based on level
            move = MO(MT.MOVE_MINIONS, (minion, None))  # Placeholder
            options.append((move,))

    return options


def generate_recruit_minion_options(
    game: WotrGame,
) -> List[ActionChoice]:
    """
    Generate options to recruit Shadow minions.

    Each minion has specific recruitment conditions on their character card.
    """
    options: List[ActionChoice] = []

    # Witch-king: Requires Sauron nation at war and at least one FP nation at war
    if game.minion_pos.get(M.WITCH_KING) is None:
        politics = getattr(game, "politics", None)
        if politics:
            sauron_at_war = politics.nations[N.MORDOR].at_war
            fp_at_war = any(politics.nations[n].at_war for n in FREE_NATIONS)
            if sauron_at_war and fp_at_war:
                # Can recruit in any region with Shadow army containing Sauron unit
                for region in game.regions:
                    if region.army and region.army.player == P.SHADOW:
                        # Check for Sauron units (mord_reg, mord_elt)
                        has_sauron = any(
                            u.name.startswith("mord") for u in region.army.units
                        )
                        if has_sauron:
                            move = MO(MT.RECRUIT_MINION, (M.WITCH_KING, region.idx))
                            options.append((move,))

    # Saruman and Mouth of Sauron have their own conditions
    # (Simplified - would need full character card implementation)

    return options


def generate_recruit_dice_companion_options(
    game: WotrGame,
) -> List[ActionChoice]:
    """
    Generate options to recruit special companions using Will of the West.

    - Aragorn - Heir to Isildur: Replaces Strider when conditions met
    - Gandalf the White: Replaces Gandalf the Grey (or enters if Grey dead)
    """
    options: List[ActionChoice] = []

    # Check for Aragorn recruitment
    # Strider must be in play and not in fellowship
    companion_pos = getattr(game, "companion_pos", {})
    strider_pos = companion_pos.get(C.STRIDER)
    if strider_pos is not None:
        move = MO(MT.RECRUIT_DICE_COMPANION, C.ARAGORN)
        options.append((move,))

    # Check for Gandalf the White recruitment
    # Gandalf Grey must be dead or in play, and a minion must be/have been in play
    gandalf_grey_pos = companion_pos.get(C.GANDALF_GREY)
    any_minion = any(pos is not None for pos in game.minion_pos.values())
    # Simplified check
    if any_minion:
        move = MO(MT.RECRUIT_DICE_COMPANION, C.GANDALF_WHITE)
        options.append((move,))

    return options


def generate_draw_card_options(
    game: WotrGame,
    player: Player,
) -> List[ActionChoice]:
    """Generate options to draw a card from either deck."""
    options: List[ActionChoice] = []

    # Can draw from Character deck or Strategy deck
    move_char = MO(MT.DRAW_CARD, "character")
    move_strat = MO(MT.DRAW_CARD, "strategy")
    options.append((move_char,))
    options.append((move_strat,))

    return options


def generate_play_card_options(
    game: WotrGame,
    player: Player,
    card_type: Optional[str] = None,
) -> List[ActionChoice]:
    """
    Generate options to play event cards.

    Args:
        game: Current game state
        player: Player playing the card
        card_type: If specified, only cards of this type can be played
                  ("character", "army", "muster", or None for any)
    """
    options: List[ActionChoice] = []

    player_state = game.player_states[player]
    hand = player_state.card_manager.hand

    for card in hand:
        # Check if card type matches required type
        if card_type:
            card_type_match = False
            if card_type == "character" and card.deck_type.name.endswith("CHARACTER"):
                card_type_match = True
            elif (
                card_type == "army"
                and "army" in str(getattr(card, "action_type", "")).lower()
            ):
                card_type_match = True
            elif (
                card_type == "muster"
                and "muster" in str(getattr(card, "action_type", "")).lower()
            ):
                card_type_match = True

            if not card_type_match and card_type != "any":
                continue

        # Check if card conditions are met
        # (Would need condition checker implementation)

        move = MO(MT.PLAY_CARD, card.idx)
        options.append((move,))

    return options


def generate_convert_die_options(
    game: WotrGame,
    player: Player,
) -> List[ActionChoice]:
    """Generate options to convert Will of the West to another die result."""
    options: List[ActionChoice] = []

    # Can convert to any result except Eye
    for result in [A.CHARACTER, A.ARMY, A.MUSTER, A.PALANTIR, A.HYBRID]:
        move = MO(MT.CONVERT_TO_WOTW, result)
        options.append((move,))

    return options


def generate_pass_option() -> List[ActionChoice]:
    """Generate the pass/skip action option."""
    move = MO(MT.PASS, None)
    return [(move,)]


# ============================================================================
# MAIN ACTION DIE RESOLUTION
# ============================================================================


@dataclass
class DieResolutionContext:
    """Context for resolving an action die."""

    game: WotrGame
    player: Player
    die_result: ActionResult
    die_index: int


def generate_die_resolution_options(
    context: DieResolutionContext,
    flatten: bool = True,
) -> ActionSpace:
    """
    Generate all possible actions for a given die result.

    Args:
        context: The die resolution context
        flatten: If True, return all options flattened; if False, return tree structure

    Returns:
        ActionSpace with all valid action choices
    """
    game = context.game
    player = context.player
    die_result = context.die_result

    all_options: List[ActionChoice] = []

    # Get available action types for this die
    if player == P.FREE:
        action_types = FP_DIE_ACTIONS.get(die_result, [])
    else:
        action_types = SHADOW_DIE_ACTIONS.get(die_result, [])

    # Generate options for each action type
    for action_type in action_types:
        if action_type == MT.MOVE_ARMY:
            requires_leader = die_result == A.CHARACTER
            max_armies = 1 if die_result == A.CHARACTER else 2
            options = define_half_move_options(
                game, player, requires_leader, max_armies
            )
            all_options.extend(options)

        elif action_type == MT.ATTACK:
            requires_leader = die_result == A.CHARACTER
            options = generate_attack_options(game, player, requires_leader)
            all_options.extend(options)

        elif action_type == MT.MUSTER:
            options = define_muster_options(game, player)
            all_options.extend(options)

        elif action_type == MT.ADVANCE_NATION_POLITICS:
            options = generate_diplomacy_options(game, player)
            all_options.extend(options)

        elif action_type == MT.MOVE_FELLOWSHIP:
            if player == P.FREE:
                options = generate_fellowship_move_options(game)
                all_options.extend(options)

        elif action_type == MT.HIDE_FELLOWSHIP:
            if player == P.FREE:
                options = generate_hide_fellowship_options(game)
                all_options.extend(options)

        elif action_type == MT.SEPARATE_COMPANIONS:
            if player == P.FREE:
                options = generate_separate_companions_options(game)
                all_options.extend(options)

        elif action_type == MT.MOVE_COMPANIONS:
            if player == P.FREE:
                options = generate_move_companions_options(game)
                all_options.extend(options)

        elif action_type == MT.MOVE_MINIONS:
            if player == P.SHADOW:
                options = generate_move_minions_options(game)
                all_options.extend(options)

        elif action_type == MT.RECRUIT_MINION:
            if player == P.SHADOW:
                options = generate_recruit_minion_options(game)
                all_options.extend(options)

        elif action_type == MT.RECRUIT_DICE_COMPANION:
            if player == P.FREE:
                options = generate_recruit_dice_companion_options(game)
                all_options.extend(options)

        elif action_type == MT.DRAW_CARD:
            options = generate_draw_card_options(game, player)
            all_options.extend(options)

        elif action_type == MT.PLAY_CARD:
            # Determine which card types can be played based on die
            if die_result == A.CHARACTER:
                card_type = "character"
            elif die_result == A.ARMY:
                card_type = "army"
            elif die_result == A.MUSTER:
                card_type = "muster"
            elif die_result == A.PALANTIR:
                card_type = "any"
            elif die_result == A.HYBRID:
                card_type = "army"  # or muster - would need to check card type
            else:
                card_type = None

            options = generate_play_card_options(game, player, card_type)
            all_options.extend(options)

        elif action_type == MT.CONVERT_TO_WOTW:
            if player == P.FREE and die_result == A.WILL:
                options = generate_convert_die_options(game, player)
                all_options.extend(options)

    # Always add pass option (if player has fewer dice than opponent)
    # This would need dice count comparison
    all_options.extend(generate_pass_option())

    return ActionSpace(tuple(all_options), 1)


def generate_sequential_die_choice(
    game: WotrGame,
    player: Player,
) -> ActionSpace:
    """
    Generate the first-level choice: which die to use.

    Returns ActionSpace with one option per unused die.
    """
    dice_pool = game.player_states[player].dice_pool.action_dice

    options: List[ActionChoice] = []
    for i, die in enumerate(dice_pool):
        if not die.action_used and die.current_result != A.EYE:
            move = MO(MT.RESOLVE_ACTION_DIE, i)
            options.append((move,))

    return ActionSpace(tuple(options), 1)


# ============================================================================
# MAIN INTERFACE FUNCTIONS (for MovesGenerator integration)
# ============================================================================


def define_options_resolve_die(game: WotrGame) -> MoveOptionSet:
    """
    Define options for resolving an action die.

    This is called by the MovesGenerator when MT.RESOLVE_ACTION_DIE is triaged.
    Returns options for selecting which die to use.
    """
    player = game.active_die_player

    # Generate choice of which die to use
    dice_pool = game.player_states[player].dice_pool.action_dice

    options: List[MoveOption] = []
    for i, die in enumerate(dice_pool):
        if not die.action_used and die.current_result != A.EYE:
            options.append(MoveOption(MT.RESOLVE_ACTION_DIE, i))

    return MoveOptionSet(tuple(options))


def execute_resolve_die(game: WotrGame, die_index: int):
    """
    Execute the selection of a die to use.

    This marks the die as used and triggers the action selection phase.
    """
    player = game.active_die_player
    dice_pool = game.player_states[player].dice_pool.action_dice

    die = dice_pool[die_index]
    die.use_die()

    # Mark that this die has been used
    # The specific action will be executed by a subsequent move


# ============================================================================
# FLATTENED OPTIONS (ALL DICE + ALL ACTIONS)
# ============================================================================


def generate_all_die_actions_flattened(
    game: WotrGame,
    player: Player,
) -> ActionSpace:
    """
    Generate a completely flattened list of all possible actions across all dice.

    Each option is a tuple of (die_selection, ...action_moves).
    This is useful for MCTS or other systems that want all options at once.
    """
    all_options: List[ActionChoice] = []
    dice_pool = game.player_states[player].dice_pool.action_dice

    for i, die in enumerate(dice_pool):
        if die.action_used or die.current_result == A.EYE:
            continue

        context = DieResolutionContext(
            game=game,
            player=player,
            die_result=die.current_result,
            die_index=i,
        )

        action_space = generate_die_resolution_options(context)

        # Prepend die selection to each action
        for action_choice in action_space.action_set:
            die_move = MO(MT.RESOLVE_ACTION_DIE, i)
            combined = (die_move,) + action_choice
            all_options.append(combined)

    return ActionSpace(tuple(all_options), 1)


# ============================================================================
# EXECUTION FUNCTIONS
# ============================================================================


def execute_move_army(game: WotrGame, move_target: Tuple[R, R]):
    """Execute army movement from source to destination."""
    source_idx, dest_idx = move_target
    source = game.regions[source_idx]
    dest = game.regions[dest_idx]

    # Move all units from source to destination
    if source.army:
        if dest.army:
            # Merge armies
            dest.units += source.units
        else:
            dest.units = source.units.copy()

        # Move characters
        dest.companions = dest.companions.union(source.companions)
        dest.minions = dest.minions.union(source.minions)
        dest.nazgul += source.nazgul

        # Clear source
        source.units.clear()
        source.companions.clear()
        source.minions.clear()
        source.nazgul = 0

        # Update armies
        source.update_army()
        dest.update_army()


def execute_attack(game: WotrGame, move_target: Tuple[R, R]):
    """Initiate a battle between attacking and defending armies."""
    attacker_idx, defender_idx = move_target
    # Would trigger battle resolution system
    # For now, placeholder
    pass


def execute_muster(game: WotrGame, move_target: Tuple):
    """Execute mustering of units."""
    region_idx, unit_type, count = move_target
    region = game.regions[region_idx]

    # Would need to determine unit type based on region's nation
    # and add appropriate units
    pass


def execute_advance_politics(game: WotrGame, nation: Nation):
    """Advance a nation on the political track."""
    politics = getattr(game, "politics", None)
    if politics:
        politics.advance_nation(nation)


def execute_fellowship_move(game: WotrGame, move_target):
    """Move the fellowship one step forward."""
    game.fellowship.move()


def execute_hide_fellowship(game: WotrGame, move_target):
    """Hide a revealed fellowship."""
    game.fellowship.revealed = False


def execute_draw_card(game: WotrGame, deck_type: str):
    """Draw a card from the specified deck."""
    player = game.active_die_player
    player_state = game.player_states[player]
    if deck_type == "character":
        player_state.card_manager.draw_cards_move(1, 0)
    else:
        player_state.card_manager.draw_cards_move(0, 1)


def execute_pass(game: WotrGame, move_target):
    """Execute pass action - do nothing but use the die."""
    pass


# Action executor mapping
DIE_ACTION_EXECUTORS = {
    MT.RESOLVE_ACTION_DIE: execute_resolve_die,
    MT.MOVE_ARMY: execute_move_army,
    MT.ATTACK: execute_attack,
    MT.MUSTER: execute_muster,
    MT.ADVANCE_NATION_POLITICS: execute_advance_politics,
    MT.MOVE_FELLOWSHIP: execute_fellowship_move,
    MT.HIDE_FELLOWSHIP: execute_hide_fellowship,
    MT.DRAW_CARD: execute_draw_card,
    MT.PASS: execute_pass,
    # Add more as needed
}
