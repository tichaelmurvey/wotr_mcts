"""
Main interface class coordinating all UI components for War of the Ring.
"""

from typing import TYPE_CHECKING, Optional, Tuple
import pygame

from game_env.regions_enum import R
from pygame_interface.config import (
    Colors,
    SIDEBAR_WIDTH_PERCENT,
    CARD_PANEL_HEIGHT,
    ACTION_PANEL_HEIGHT,
    BOARD_MARGIN,
    InteractionState,
    FPS,
)
from game_env.moves.move_types import MoveType
from pygame_interface.assets import get_asset_manager
from pygame_interface.components.board import Board
from pygame_interface.components.regions import RegionManager
from pygame_interface.components.sidebar import Sidebar
from pygame_interface.components.card_panel import CardPanel
from pygame_interface.components.action_panel import ActionPanel
from pygame_interface.components.reinforcement_pool import ReinforcementPool
from pygame_interface.components.combat_dice import CombatDice
from pygame_interface.components.dialogs import DialogManager
from pygame_interface.input_handler import InputHandler
from pygame_interface.move_builder import MoveBuilder
from pygame_interface.state_renderer import StateRenderer

if TYPE_CHECKING:
    from game_env.game_env import WotrGame
    from game_env.moves.move_types import ActionChoice, ActionSpace


class WotrInterface:
    """
    Main coordinator class for the War of the Ring pygame interface.

    Manages all UI components, handles events, and coordinates between
    the game engine and the visual display.
    """
    hovered_region : None | R
    selected_region  : None | R
    board : Board
    sidebar : Sidebar
    card_panel : CardPanel
    action_panel  : ActionPanel
    reinforcement_pool  : ReinforcementPool
    combat_dice  : CombatDice
    dialog_manager  : DialogManager
    input_handler  : InputHandler
    move_builder  : MoveBuilder
    state_renderer  : StateRenderer
    interaction_state  : InteractionState
    current_action_space: Optional["ActionSpace"]
    pending_move: Optional["ActionChoice"]
    valid_destinations  : set
    message: Optional[str]
    message_timer:float
    debug: bool
    def __init__(
        self,
        screen: pygame.Surface,
        game: Optional["WotrGame"] = None,
        debug: bool = False
    ):
        self.debug = debug
        if self.debug: print("init wotrinterface")
        """
        Initialize the interface.

        Args:
            screen: The main pygame display surface
            game: Optional WotrGame instance to connect to
        """
        self.screen = screen
        self.game = game
        self.assets = get_asset_manager()

        # Calculate initial layout
        self._calculate_layout()

        # Initialize components
        self.region_manager = RegionManager()
        self.board = Board(self.board_rect, self.region_manager)
        self.sidebar = Sidebar(self.sidebar_rect)
        self.card_panel = CardPanel(self.card_panel_rect)
        self.action_panel = ActionPanel(self.action_panel_rect)
        self.reinforcement_pool = ReinforcementPool()
        self.combat_dice = CombatDice()
        self.dialog_manager = DialogManager(screen)

        # Input handling
        self.input_handler = InputHandler(self)
        self.move_builder = MoveBuilder(self)

        # State rendering
        self.state_renderer = StateRenderer(self)

        # Interaction state
        self.interaction_state = InteractionState.IDLE
        self.current_action_space: Optional["ActionSpace"] = None
        self.pending_move: Optional["ActionChoice"] = None

        # Visual state
        self.hovered_region = None
        self.selected_region = None
        self.valid_destinations = set()
        self.message: Optional[str] = None
        self.message_timer: float = 0

        # Update state from game if provided
        if game:
            self.state_renderer.update_from_game(game)

    def _calculate_layout(self):
        """Calculate the layout rectangles for all UI components."""
        width, height = self.screen.get_size()

        # Sidebar on the right
        sidebar_width = int(width * SIDEBAR_WIDTH_PERCENT)

        # Card panel at the bottom (full width)
        card_panel_top = height - CARD_PANEL_HEIGHT - ACTION_PANEL_HEIGHT

        # Action panel at the very bottom
        action_panel_top = height - ACTION_PANEL_HEIGHT

        # Board area (left side, above card panel)
        board_width = width - sidebar_width - BOARD_MARGIN
        board_height = card_panel_top - BOARD_MARGIN

        # Store rectangles
        self.board_rect = pygame.Rect(
            BOARD_MARGIN,
            BOARD_MARGIN,
            board_width - BOARD_MARGIN,
            board_height - BOARD_MARGIN,
        )
        self.sidebar_rect = pygame.Rect(
            width - sidebar_width,
            0,
            sidebar_width,
            card_panel_top,
        )
        self.card_panel_rect = pygame.Rect(
            0,
            card_panel_top,
            width,
            CARD_PANEL_HEIGHT,
        )
        self.action_panel_rect = pygame.Rect(
            0,
            action_panel_top,
            width,
            ACTION_PANEL_HEIGHT,
        )

    def handle_resize(self, width: int, height: int):
        """
        Handle window resize event.

        Args:
            width: New window width
            height: New window height
        """
        self._calculate_layout()

        # Update component layouts
        self.board.set_rect(self.board_rect)
        self.sidebar.set_rect(self.sidebar_rect)
        self.card_panel.set_rect(self.card_panel_rect)
        self.action_panel.set_rect(self.action_panel_rect)

    def handle_event(self, event: pygame.event.Event):
        """
        Handle a pygame event.

        Args:
            event: The pygame event to handle
        """
        # Check if dialog should handle event first
        if self.dialog_manager.is_open():
            self.dialog_manager.handle_event(event)
            return

        # Delegate to input handler
        self.input_handler.handle_event(event)

    def update(self):
        """Update the interface state (called each frame)."""
        # Update message timer
        if self.message and self.message_timer > 0:
            self.message_timer -= 1 / FPS
            if self.message_timer <= 0:
                self.message = None

        # Update components
        self.board.update()
        self.sidebar.update()
        self.card_panel.update()
        self.action_panel.update()
        self.dialog_manager.update()

    def draw(self):
        """Draw all interface components."""
        # Clear screen
        self.screen.fill(Colors.BACKGROUND)

        # Draw main components
        self.board.draw(self.screen)
        self.sidebar.draw(self.screen)
        self.card_panel.draw(self.screen)
        self.action_panel.draw(self.screen)

        # Draw message if present
        if self.message:
            self._draw_message()

        # Draw dialogs on top
        self.dialog_manager.draw()

    def _draw_message(self):
        """Draw a temporary message on screen."""
        if not self.message:
            return

        font = self.assets.get_font(24)
        text = font.render(self.message, True, Colors.TEXT_PRIMARY)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))

        # Draw background
        padding = 10
        bg_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(self.screen, Colors.PANEL_BG, bg_rect)
        pygame.draw.rect(self.screen, Colors.PANEL_BORDER, bg_rect, 2)

        # Draw text
        self.screen.blit(text, text_rect)

    def show_message(self, text: str, duration: float = 3.0):
        """
        Show a temporary message to the user.

        Args:
            text: Message to display
            duration: How long to show the message in seconds
        """
        self.message = text
        self.message_timer = duration

    def update_game_state(self, game: "WotrGame"):
        """
        Update the interface to reflect the current game state.

        Args:
            game: The WotrGame instance to read state from
        """
        self.game = game
        self.state_renderer.update_from_game(game)

    def get_player_move(
        self,
        action_space: "ActionSpace",
    ) -> Optional["ActionChoice"]:
        """
        Wait for and return a player's move selection.

        This method should be called when the game engine needs player input.
        It blocks until the player makes a valid move selection.

        Args:
            action_space: The available actions the player can choose from

        Returns:
            The selected ActionChoice, or None if cancelled
        """
        if self.debug: print("get_player_move")

        self.current_action_space = action_space
        self.pending_move = None
        self.move_builder.set_action_space(action_space)

        # Set interaction state based on action space
        self.interaction_state = InteractionState.SELECTING_SOURCE

        # Update sidebar with awaited move description
        awaited_description = self._get_awaited_move_description(action_space)
        self.sidebar.set_awaited_move(awaited_description)

        # Block until move is made
        clock = pygame.time.Clock()
        while self.pending_move is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.VIDEORESIZE:
                    width = max(event.w, 1280)
                    height = max(event.h, 720)
                    self.screen = pygame.display.set_mode(
                        (width, height),
                        pygame.RESIZABLE,
                    )
                    self.handle_resize(width, height)
                else:
                    self.handle_event(event)

            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

        # Reset state
        self.current_action_space = None
        self.interaction_state = InteractionState.IDLE
        self.move_builder.reset()
        self.sidebar.set_awaited_move(None)

        return self.pending_move

    def submit_move(self, move: "ActionChoice"):
        """
        Submit a completed move (called by MoveBuilder).

        Args:
            move: The ActionChoice to submit
        """
        self.pending_move = move

    def cancel_selection(self):
        """Cancel the current selection and reset interaction state."""
        self.selected_region = None
        self.valid_destinations = set()
        self.interaction_state = InteractionState.SELECTING_SOURCE
        self.move_builder.reset()

    def set_valid_destinations(self, destinations: set):
        """
        Set the valid destination regions for highlighting.

        Args:
            destinations: Set of R enum values for valid destinations
        """
        self.valid_destinations = destinations
        self.board.set_highlighted_regions(destinations, Colors.HIGHLIGHT_VALID_MOVE)

    def get_region_at_pos(self, pos: Tuple[int, int]):
        """
        Get the region at a screen position.

        Args:
            pos: Screen (x, y) position

        Returns:
            R enum value of region at position, or None
        """
        # Convert screen position to board position
        board_pos = self.board.screen_to_board_pos(pos)
        if board_pos is None:
            return None

        return self.region_manager.get_region_at_pos(
            board_pos,
            self.board.get_board_size(),
        )

    def highlight_region(self, region, color=None):
        """
        Highlight a specific region.

        Args:
            region: R enum value of region to highlight
            color: Optional color override
        """
        if region:
            self.board.highlight_region(
                region,
                color or Colors.HIGHLIGHT_SELECTED,
            )

    def clear_highlights(self):
        """Clear all region highlights."""
        self.board.clear_highlights()
        self.valid_destinations = set()

    def _get_move_type_description(self, move_type: MoveType) -> str:
        """Get a human-readable description for a move type."""
        descriptions = {
            MoveType.EVENT_CARD_DISCARD: "Card Discard",
            MoveType.RESOLVE_ACTION_DIE: "Action Die",
            MoveType.CHOOSE_COMBAT_CARD: "Combat Card",
            MoveType.CHANGE_GUIDE: "Guide Change",
            MoveType.RESOLVE_HUNT_DAMAGE: "Hunt Damage",
            MoveType.DECLARE_FELLOWSHIP: "Fellowship Declaration",
            MoveType.REVEAL_FELLOWSHIP: "Fellowship Reveal",
            MoveType.USE_HUNT_TABLE_CARD: "Hunt Card",
            MoveType.USE_GUIDE_HUNT_ABILITY: "Guide Ability",
            MoveType.SHADOWS_GATHER: "Shadows Gather",
        }
        return descriptions.get(move_type, move_type.name.replace("_", " ").title())

    def _get_awaited_move_description(self, action_space: "ActionSpace") -> str:
        """Get a description of what move is being awaited from an action space."""
        if not action_space or not action_space.action_set:
            return "Input"

        # Collect all move types from the action space
        move_types = set()
        for action_choice in action_space.action_set:
            if action_choice:
                for move in action_choice:
                    move_types.add(move.move_type)

        if len(move_types) == 1:
            return self._get_move_type_description(list(move_types)[0])
        elif len(move_types) > 1:
            # Return the most relevant/common one
            for priority_type in [
                MoveType.RESOLVE_ACTION_DIE,
                MoveType.EVENT_CARD_DISCARD,
                MoveType.DECLARE_FELLOWSHIP,
                MoveType.CHANGE_GUIDE,
                MoveType.CHOOSE_COMBAT_CARD,
            ]:
                if priority_type in move_types:
                    return self._get_move_type_description(priority_type)
            return f"{len(move_types)} move types"

        return "Input"
