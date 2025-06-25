import pygame
import sys

from screen import Screen
from button import Button

from classic_game_mode import ClassicGameMode

class GameModes(Screen):
    """
    A screen that allows the user to choose between different game modes.
    Inherits from the base Screen class and uses buttons for interaction.
    """

    def __init__(self, menu, manager, settings):
        """
        Initializes the GameModes screen.

        Args:
            menu: Reference to the main menu screen, used for returning.
            manager: Screen manager to handle screen switching.
            settings: Global game settings and screen references.
        """
        super().__init__(manager)

        # Game and screen settings
        self.settings = settings
        self.screen = settings.screen
        self.screen_rect = settings.screen_rect
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        self.bg_surface = settings.bg_surface

        self.menu = menu

        # Button labels to be displayed
        self.buttons_msgs = [
            "classic",
            "coming soon",
            "return"
        ]

        # Create and position buttons based on messages
        self.buttons = self._create_buttons()

    def _create_buttons(self):
        """
        Creates button objects with vertical spacing and centers them on screen.

        Returns:
            list: A list of Button instances.
        """
        buttons = []
        offset = 0
        start_pos = self.screen_rect.center
        for button_msg in self.buttons_msgs:
            new_button = Button(self, button_msg, position=start_pos, offset_y=offset)
            offset += new_button.rect.height * 1.5  # Vertical spacing between buttons
            buttons.append(new_button)
        return buttons

    def _check_event(self):
        """
        Checks for and processes user input events like quit, key press, or mouse click.
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
        Determines if a button was clicked and switches screens accordingly.

        Args:
            click_pos (tuple): The (x, y) position of the mouse click.
        """
        for button in self.buttons:
            if button.rect.collidepoint(click_pos):
                if button.message == "return":
                    self.manager.switch_screen(self.menu)
                elif button.message == "classic":
                    self.manager.switch_screen(ClassicGameMode(self.manager, self.settings, self.menu))

    def _update_screen(self):
        """
        Draws the background and all buttons, and updates the display.
        """
        self.screen.blit(self.bg_surface, (0, 0))

        for button in self.buttons:
            button.draw_button()
        
        pygame.display.flip()