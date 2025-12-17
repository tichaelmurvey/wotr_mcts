from game_env.game_env import WotrGame
from pygame_interface.main import run_with_game


game = WotrGame(verbose=True)
run_with_game(game)