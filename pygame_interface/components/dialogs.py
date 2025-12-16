"""
Dialog components for War of the Ring interface.

Provides modal dialogs for card details, confirmations, and special actions.
"""

from typing import Callable, List, Optional, Tuple
import pygame

from pygame_interface.config import (
    Colors,
    FONT_SIZE_LARGE,
    FONT_SIZE_MEDIUM,
    FONT_SIZE_SMALL,
    BUTTON_HEIGHT,
)
from pygame_interface.assets import get_asset_manager


class Dialog:
    """Base class for modal dialogs."""

    def __init__(
        self,
        screen: pygame.Surface,
        title: str,
        width: int = 400,
        height: int = 300,
    ):
        """
        Initialize a dialog.

        Args:
            screen: The main screen surface
            title: Dialog title
            width: Dialog width
            height: Dialog height
        """
        self.screen = screen
        self.title = title
        self.assets = get_asset_manager()

        # Calculate centered position
        screen_rect = screen.get_rect()
        self.rect = pygame.Rect(
            (screen_rect.width - width) // 2,
            (screen_rect.height - height) // 2,
            width,
            height,
        )

        self.visible = False
        self.result: Optional[str] = None

        # Callbacks
        self.on_close: Optional[Callable[[Optional[str]], None]] = None

    def show(self):
        """Show the dialog."""
        self.visible = True
        self.result = None

    def close(self, result: Optional[str] = None):
        """Close the dialog with an optional result."""
        self.visible = False
        self.result = result
        if self.on_close:
            self.on_close(result)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle a pygame event.

        Args:
            event: The event to handle

        Returns:
            True if the event was consumed
        """
        if not self.visible:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close(None)
                return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rect.collidepoint(event.pos):
                # Click outside - close
                self.close(None)
                return True

        return True  # Consume all events when dialog is open

    def update(self):
        """Update dialog state."""
        pass

    def draw(self):
        """Draw the dialog."""
        if not self.visible:
            return

        # Dim background
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Draw dialog background
        pygame.draw.rect(self.screen, Colors.PANEL_BG, self.rect)
        pygame.draw.rect(self.screen, Colors.PANEL_BORDER, self.rect, 2)

        # Draw title bar
        title_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            30,
        )
        pygame.draw.rect(self.screen, Colors.DARK_GRAY, title_rect)

        font = self.assets.get_font(FONT_SIZE_MEDIUM)
        title_text = font.render(self.title, True, Colors.TEXT_PRIMARY)
        self.screen.blit(title_text, (self.rect.x + 10, self.rect.y + 5))


class ConfirmDialog(Dialog):
    """Confirmation dialog with Yes/No buttons."""

    def __init__(
        self,
        screen: pygame.Surface,
        title: str,
        message: str,
        yes_text: str = "Yes",
        no_text: str = "No",
    ):
        super().__init__(screen, title, width=350, height=150)
        self.message = message
        self.yes_text = yes_text
        self.no_text = no_text

        # Button rects
        button_width = 80
        button_y = self.rect.bottom - 50
        self.yes_rect = pygame.Rect(
            self.rect.centerx - button_width - 10,
            button_y,
            button_width,
            BUTTON_HEIGHT,
        )
        self.no_rect = pygame.Rect(
            self.rect.centerx + 10,
            button_y,
            button_width,
            BUTTON_HEIGHT,
        )

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.yes_rect.collidepoint(event.pos):
                self.close("yes")
                return True
            elif self.no_rect.collidepoint(event.pos):
                self.close("no")
                return True

        return super().handle_event(event)

    def draw(self):
        if not self.visible:
            return

        super().draw()

        font = self.assets.get_font(FONT_SIZE_SMALL)

        # Draw message
        message_text = font.render(self.message, True, Colors.TEXT_PRIMARY)
        message_rect = message_text.get_rect(
            centerx=self.rect.centerx,
            top=self.rect.y + 50,
        )
        self.screen.blit(message_text, message_rect)

        # Draw buttons
        self._draw_button(self.yes_rect, self.yes_text, Colors.FREE_PEOPLES)
        self._draw_button(self.no_rect, self.no_text, Colors.SHADOW)

    def _draw_button(
        self,
        rect: pygame.Rect,
        text: str,
        color: Tuple[int, int, int],
    ):
        """Draw a button."""
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, Colors.PANEL_BORDER, rect, 1)

        font = self.assets.get_font(FONT_SIZE_SMALL)
        text_surface = font.render(text, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)


class SelectionDialog(Dialog):
    """Dialog for selecting from a list of options."""

    def __init__(
        self,
        screen: pygame.Surface,
        title: str,
        options: List[str],
    ):
        height = min(400, 80 + len(options) * 30)
        super().__init__(screen, title, width=350, height=height)
        self.options = options
        self.option_rects: List[pygame.Rect] = []
        self.hovered_index: Optional[int] = None
        self._calculate_option_rects()

    def _calculate_option_rects(self):
        """Calculate clickable rects for each option."""
        self.option_rects.clear()
        y = self.rect.y + 40
        padding = 10

        for i in range(len(self.options)):
            rect = pygame.Rect(
                self.rect.x + padding,
                y,
                self.rect.width - padding * 2,
                25,
            )
            self.option_rects.append(rect)
            y += 30

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered_index = None
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.hovered_index = i
                    break

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.close(self.options[i])
                    return True

        return super().handle_event(event)

    def draw(self):
        if not self.visible:
            return

        super().draw()

        font = self.assets.get_font(FONT_SIZE_SMALL)

        for i, (option, rect) in enumerate(zip(self.options, self.option_rects)):
            # Highlight hovered option
            if i == self.hovered_index:
                pygame.draw.rect(self.screen, Colors.DARK_GRAY, rect)

            text = font.render(option, True, Colors.TEXT_PRIMARY)
            self.screen.blit(text, (rect.x + 5, rect.y + 3))


class MessageDialog(Dialog):
    """Simple message dialog with OK button."""

    def __init__(
        self,
        screen: pygame.Surface,
        title: str,
        message: str,
    ):
        super().__init__(screen, title, width=350, height=130)
        self.message = message

        # OK button
        button_width = 80
        self.ok_rect = pygame.Rect(
            self.rect.centerx - button_width // 2,
            self.rect.bottom - 45,
            button_width,
            BUTTON_HEIGHT,
        )

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.ok_rect.collidepoint(event.pos):
                self.close("ok")
                return True

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.close("ok")
            return True

        return super().handle_event(event)

    def draw(self):
        if not self.visible:
            return

        super().draw()

        font = self.assets.get_font(FONT_SIZE_SMALL)

        # Draw message
        message_text = font.render(self.message, True, Colors.TEXT_PRIMARY)
        message_rect = message_text.get_rect(
            centerx=self.rect.centerx,
            top=self.rect.y + 45,
        )
        self.screen.blit(message_text, message_rect)

        # Draw OK button
        pygame.draw.rect(self.screen, Colors.PANEL_BORDER, self.ok_rect)
        pygame.draw.rect(self.screen, Colors.WHITE, self.ok_rect, 1)

        ok_text = font.render("OK", True, Colors.TEXT_PRIMARY)
        ok_text_rect = ok_text.get_rect(center=self.ok_rect.center)
        self.screen.blit(ok_text, ok_text_rect)


class DialogManager:
    """Manages dialog display and lifecycle."""

    def __init__(self, screen: pygame.Surface):
        """
        Initialize the dialog manager.

        Args:
            screen: The main screen surface
        """
        self.screen = screen
        self.current_dialog: Optional[Dialog] = None

    def is_open(self) -> bool:
        """Check if any dialog is currently open."""
        return self.current_dialog is not None and self.current_dialog.visible

    def show_message(
        self,
        title: str,
        message: str,
        callback: Optional[Callable] = None,
    ):
        """
        Show a message dialog.

        Args:
            title: Dialog title
            message: Message to display
            callback: Optional callback when closed
        """
        dialog = MessageDialog(self.screen, title, message)
        dialog.on_close = callback
        dialog.show()
        self.current_dialog = dialog

    def show_confirm(
        self,
        title: str,
        message: str,
        callback: Optional[Callable[[Optional[str]], None]] = None,
        yes_text: str = "Yes",
        no_text: str = "No",
    ):
        """
        Show a confirmation dialog.

        Args:
            title: Dialog title
            message: Message to display
            callback: Callback receiving "yes", "no", or None
            yes_text: Text for yes button
            no_text: Text for no button
        """
        dialog = ConfirmDialog(self.screen, title, message, yes_text, no_text)
        dialog.on_close = callback
        dialog.show()
        self.current_dialog = dialog

    def show_selection(
        self,
        title: str,
        options: List[str],
        callback: Optional[Callable[[Optional[str]], None]] = None,
    ):
        """
        Show a selection dialog.

        Args:
            title: Dialog title
            options: List of options to choose from
            callback: Callback receiving selected option or None
        """
        dialog = SelectionDialog(self.screen, title, options)
        dialog.on_close = callback
        dialog.show()
        self.current_dialog = dialog

    def close(self):
        """Close the current dialog."""
        if self.current_dialog:
            self.current_dialog.close()
            self.current_dialog = None

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle an event.

        Args:
            event: The pygame event

        Returns:
            True if the event was consumed
        """
        if self.current_dialog:
            result = self.current_dialog.handle_event(event)
            if not self.current_dialog.visible:
                self.current_dialog = None
            return result
        return False

    def update(self):
        """Update the current dialog."""
        if self.current_dialog:
            self.current_dialog.update()
            if not self.current_dialog.visible:
                self.current_dialog = None

    def draw(self):
        """Draw the current dialog."""
        if self.current_dialog:
            self.current_dialog.draw()
