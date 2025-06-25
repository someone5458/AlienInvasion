import pygame
import sys

from screen import Screen
from button import Button
from game_modes import GameModes
from statistics_screen import Statistics

class Menu(Screen):
    """
    Main menu screen class. Displays the main menu and handles user interaction with it.
    """

    def __init__(self, manager, settings):
        """
        Initializes the Menu screen with background, buttons, and screen settings.

        Args:
            manager: The screen manager responsible for switching between screens.
            settings: The global game settings object.
        """
        super().__init__(manager)

        self.settings = settings
        self.screen = settings.screen
        self.screen_rect = settings.screen_rect
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        self.bg_surface = settings.bg_surface  # Background surface for the menu

        # Button labels to be displayed in the menu
        self.menu_buttons_msgs = [
            "play",
            "statistics",
            "exit",
        ]

        self.menu_buttons = self._create_buttons()  # Create button instances

    def _create_buttons(self):
        """
        Creates and positions the menu buttons on the screen.

        Returns:
            A list of Button objects.
        """
        buttons = []
        offset = 0
        start_pos = self.screen_rect.center

        for button_msg in self.menu_buttons_msgs:
            new_button = Button(self, button_msg, position=start_pos, offset_y=offset)
            offset += new_button.rect.height * 1.5  # Add spacing between buttons
            buttons.append(new_button)
        return buttons

    def _check_event(self):
        """
        Handles all user input events, including quitting, keyboard, and mouse interactions.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)

    def _check_buttons(self, click_pos):
        """
        Handles logic when a button is clicked.

        Args:
            click_pos: Tuple of (x, y) mouse coordinates.
        """
        for button in self.menu_buttons:
            if button.rect.collidepoint(click_pos):
                if button.message == "exit":
                    sys.exit()
                elif button.message == "play":
                    # Switch to the GameModes screen
                    self.manager.switch_screen(GameModes(self, self.manager, self.settings))
                elif button.message == "statistics":
                    self.manager.switch_screen(Statistics(self, self.manager, self.settings))

    def _update_screen(self):
        """
        Renders the menu background and all buttons, then updates the display.
        """
        self.screen.blit(self.bg_surface, (0, 0))

        for button in self.menu_buttons:
            button.draw_button()

        pygame.display.flip()









