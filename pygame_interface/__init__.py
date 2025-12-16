"""
War of the Ring Pygame Interface

A pygame-based interface for War of the Ring (2nd Edition) that:
- Reads game state from game_env and renders the map, units, cards, and game assets
- Handles player input and translates them to ActionChoice tuples
- Does NOT implement game logic (that lives in game_env)
"""

from pygame_interface.game_interface import WotrInterface

__all__ = ["WotrInterface"]
