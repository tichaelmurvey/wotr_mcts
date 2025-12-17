"""
Main entry point for the War of the Ring pygame interface.
"""

import sys
import pygame

from game_env.game_env import WotrGame
from pygame_interface.config import (
    WINDOW_TITLE,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT,
    FPS,
)

from pygame_interface.assets import init_assets
from pygame_interface.game_interface import WotrInterface


def main():
    """Main entry point for running the interface standalone."""
    # Initialize pygame
    pygame.init()
    pygame.font.init()

    # Set up display
    screen = pygame.display.set_mode(
        (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT),
        pygame.RESIZABLE,
    )
    pygame.display.set_caption(WINDOW_TITLE)

    # Initialize asset manager
    init_assets()

    # Create the interface (no game instance for standalone mode)
    interface = WotrInterface(screen)

    # Main loop
    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Enforce minimum window size
                width = max(event.w, MIN_WINDOW_WIDTH)
                height = max(event.h, MIN_WINDOW_HEIGHT)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                interface.handle_resize(width, height)
            else:
                interface.handle_event(event)

        # Update
        interface.update()

        # Draw
        interface.draw()
        pygame.display.flip()

        # Cap framerate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def run_with_game(game: WotrGame):
    """
    Run the interface with an actual game instance.

    Args:
        game: WotrGame instance to connect to
    """
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(
        (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT),
        pygame.RESIZABLE,
    )
    pygame.display.set_caption(WINDOW_TITLE)

    init_assets()

    interface = WotrInterface(screen, game, debug=True)

    # Main loop
    clock = pygame.time.Clock()
    running = True

    # Start game
    game.start_game(verbose=True)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Enforce minimum window size
                width = max(event.w, MIN_WINDOW_WIDTH)
                height = max(event.h, MIN_WINDOW_HEIGHT)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                interface.handle_resize(width, height)
            else:
                interface.handle_event(event)

        # Update game state display
        interface.update_game_state(game)

        # Check if game needs player input
        if hasattr(game, 'current_action_space') and game.current_action_space:
            # Get player move through the interface
            move = interface.get_player_move(game.current_action_space)
            if move is None:
                # Player closed the window during move selection
                running = False
            else:
                # Apply the move and progress the game
                game.implement_player_action(move)

        # Update interface
        interface.update()

        # Draw
        interface.draw()
        pygame.display.flip()

        # Cap framerate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
