from typing import List

from game_env.moves.move_types import (
    MT,
    ActionChoiceSet,
    MoveOption,
    MoveOptionTree,
    OptionBranch,
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


sample_tree = MoveOptionTree(
    option_branches=[
        OptionBranch(MoveOption(MT.ATTACK, "4"), None),
        OptionBranch(
            MoveOption(MT.ATTACK, "3"),
            [
                OptionBranch(MoveOption(MT.ADVANCE_NATION_POLITICS, "bar"), None),
                OptionBranch(
                    MoveOption(MT.ADVANCE_NATION_POLITICS, "foo"),
                    [
                        OptionBranch(
                            MoveOption(MT.ADVANCE_NATION_POLITICS, "phlegm"), None
                        ),
                        OptionBranch(MoveOption(MT.CHANGE_GUIDE, "pippin"), None),
                    ],
                ),
            ],
        ),
    ]
)

flat_tree = flatten_tree(sample_tree)
for sequence in flat_tree:
    seq_string = ""
    for move in sequence:
        seq_string += move.move_type.name + " " + move.move_target + " "  # type: ignore
    print(seq_string)
