from typing import TYPE_CHECKING
from game_env.moves import card_moves, define_action_die_moves, fellowship_moves

if TYPE_CHECKING:
    from game_env.moves.move_types import MT, OptionsFn

ACTION_OPTION_OBSERVERS: dict[MT, OptionsFn] = {
    MT.EVENT_CARD_DISCARD: card_moves.define_options,
    MT.CHANGE_GUIDE: fellowship_moves.define_options_guide,
    MT.DECLARE_FELLOWSHIP: fellowship_moves.define_options_declare,
    MT.HUNT_ALLOCATION: fellowship_moves.define_options_hunt_allocation,
    MT.RESOLVE_ACTION_DIE: define_action_die_moves.define_options_resolve_die,
}
