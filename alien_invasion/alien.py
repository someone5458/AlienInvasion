import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    A class to represent a single alien in the fleet.
    Manages rendering, positioning, and edge detection.
    """

    def __init__(self, ai_game):
        """
        Initialize the alien and set its starting position.

        Args:
            ai_game: The main game instance, used to access settings and screen.
        """
        super().__init__()  # Initialize base Sprite class

        self.screen = ai_game.screen  # Reference to the game screen
        self.screen_rect = self.screen.get_rect()  # Get the screen dimensions
        self.settings = ai_game.settings  # Reference to game settings

        # Load the alien image and get its rectangular hitbox
        self.image = pygame.image.load("images/alien_ship_1.png")
        self.rect = self.image.get_rect()

        # Start each new alien near the top-left of the screen, with some padding
        self.rect.x = self.rect.width  # Offset from the left edge
        self.rect.y = self.rect.height  # Offset from the top edge

        # Store the alien’s exact horizontal position as a float for smooth movement
        self.x = float(self.rect.x)

    def check_edges(self) -> bool:
        """
        Check if the alien has reached either edge of the screen.

        Returns:
            bool: True if the alien is at the left or right edge of the screen.
        """
        return self.rect.right >= self.screen_rect.right or self.rect.left <= 0

    def update(self):
        """
        Update the alien’s horizontal position based on speed and fleet direction.
        """
        # Fleet direction is either 1 (right) or -1 (left)
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    

    