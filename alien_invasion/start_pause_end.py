import pygame

from button import Button

class StartPauseEndButtons:
    """
    This class handles the creation and behavior of buttons displayed during the 
    start, pause, and end states of the game.
    """

    def __init__(self, game_cls, game):
        """
        Initialize the button handler with references to game state, manager, 
        screen, and other relevant components.
        """
        self.Game_class = game_cls
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.save_file = game.save_file

        self.manager = game.manager
        self.settings = game.settings
        self.menu = game.menu
        self.stats = game.stats

        # List of currently active (visible) buttons
        self.active_buttons = []

        # Button labels for different game states
        self.start_buttons_msgs = [
            "start",
            "main menu"
        ]
        
        self.pause_buttons_msgs = [
            "return",
            "restart",
            "main menu"
        ]

        self.end_buttons_msgs = [
            "restart",
            "main menu"
        ]

    def _check_pause(self):
        """
        Toggle the game's pause state and update visible buttons accordingly.
        """
        self.stats.game_active = not self.stats.game_active
        if not self.stats.game_active:
            self.active_buttons = self._create_buttons(self.pause_buttons_msgs)
        else:
            self.active_buttons = []
        self._update_mouse_visibility()

    def _check_start(self):
        """
        Display the start screen buttons if the game is not active.
        """
        if not self.stats.game_active:
            self.active_buttons = self._create_buttons(self.start_buttons_msgs)
        else:
            self.active_buttons = []
        self._update_mouse_visibility()

    def _check_end(self):
        """
        Display the end screen buttons and deactivate the game.
        """
        self.stats.game_active = False
        self.active_buttons = self._create_buttons(self.end_buttons_msgs)
        self._update_mouse_visibility()

    def _create_buttons(self, buttons_msgs):
        """
        Create and return a list of Button objects based on the provided messages.
        
        Args:
            buttons_msgs (list): List of button text labels.
        
        Returns:
            list: List of Button instances.
        """
        buttons = []
        button = Button(self.game, "")  # Dummy button to get dimensions
        offset = 0
        start_pos = self.screen_rect.center
        for button_msg in buttons_msgs:
            new_button = Button(self, button_msg, position=start_pos, offset_y=offset)
            offset += button.rect.height * 0.5 * 3  # Add vertical spacing
            buttons.append(new_button)
        return buttons

    def _check_buttons_events(self, mouse_pos):
        """
        Handle events when the user clicks on any of the active buttons.
        
        Args:
            mouse_pos (tuple): Current mouse position.
        """
        for button in self.active_buttons:
            clicked = button.rect.collidepoint(mouse_pos)
            if clicked:
                if button.message == "start":
                    self.stats.game_active = True
                    self._update_mouse_visibility()
                elif button.message == "return":
                    self._check_pause()
                elif button.message == "restart":
                    self.manager.switch_screen(self.Game_class(self.manager, self.settings, self.menu))
                elif button.message == "main menu":
                    self.save_file.save(self.stats)
                    self.manager.switch_screen(self.menu)

    def _update_mouse_visibility(self):
        """
        Set mouse visibility depending on whether the game is active.
        """
        pygame.mouse.set_visible(not self.stats.game_active)