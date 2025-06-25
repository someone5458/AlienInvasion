import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """
    Represents a bullet fired by an alien in the game.
    Inherits from pygame.sprite.Sprite to allow for sprite grouping and collision detection.
    """

    def __init__(self, ai_game, alien):
        """
        Initialize the alien bullet's position and appearance.

        Args:
            ai_game: The main game instance, used to access game-wide settings.
            alien: The alien sprite that is firing the bullet.
        """
        super().__init__()  # Initialize base Sprite class

        # Access game settings and assign the firing alien
        self.settings = ai_game.settings
        self.alien = alien

        # Load bullet image and set up its rectangular hitbox
        self.image = pygame.image.load("images/alien_bullet.png")
        self.rect = self.image.get_rect()

        # Position the bullet at the center-bottom of the alien
        self.rect.midtop = self.alien.rect.midbottom

        # Use a float for vertical position to allow fine movement
        self.y = float(self.rect.y)

    def update(self):
        """
        Move the bullet downward based on alien bullet speed.
        This method should be called every frame.
        """
        self.y += self.settings.alien_bullet_speed  # Move bullet down
        self.rect.y = self.y  # Update rect for rendering and collision
