from abc import ABC, abstractmethod

class Screen(ABC):
    """
    Abstract base class for all screens (menu, game modes, game screen, etc.)
    """

    def __init__(self, manager):
        self.manager = manager

    @abstractmethod
    def _check_event(self):
        """
        Handles all input events like mouse clicks or key presses.
        """
        pass

    def _update(self):
        """
        Optional method to update game logic; override if needed.
        """
        pass

    @abstractmethod
    def _update_screen(self):
        """
        Handles screen drawing. Must be implemented in subclasses.
        """
        pass