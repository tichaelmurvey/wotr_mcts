"""
UI Components for the War of the Ring interface.
"""

from pygame_interface.components.board import Board
from pygame_interface.components.regions import RegionManager
from pygame_interface.components.sidebar import Sidebar
from pygame_interface.components.card_panel import CardPanel
from pygame_interface.components.action_panel import ActionPanel
from pygame_interface.components.reinforcement_pool import ReinforcementPool
from pygame_interface.components.combat_dice import CombatDice
from pygame_interface.components.dialogs import DialogManager

__all__ = [
    "Board",
    "RegionManager",
    "Sidebar",
    "CardPanel",
    "ActionPanel",
    "ReinforcementPool",
    "CombatDice",
    "DialogManager",
]
