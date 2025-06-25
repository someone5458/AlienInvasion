import pygame
from menu import Menu


class ScreenManager():
    """
    Controls which screen (menu, gameplay, etc.) is currently active and running.
    """

    def __init__(self, settings):
        pygame.init()
        self.settings = settings

        # Get screen parameters from settings
        self.screen = self.settings.screen
        self.screen_rect = self.settings.screen_rect
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height

        self.bg_surface = self.settings.bg_surface

        # Set the initial screen to the main menu
        self.active_screen = Menu(self, self.settings)

    def run(self):
        """
        The main loop of the screen manager. Delegates control to the active screen.
        """
        while True:
            self.active_screen._check_event()     # Handle input/events
            self.active_screen._update()          # Update logic (if needed)
            self.active_screen._update_screen()   # Redraw the screen

    def switch_screen(self, new_screen):
        """
        Replaces the currently active screen with a new one.
        """
        self.active_screen = new_screen