import pygame
from random import randint
from bg_builder import BackGround
from screen_manager import ScreenManager

class Settings:
    """
    Stores and manages all game configuration values and settings.
    """

    def __init__(self):
        """
        Initializes display, gameplay settings, and resource loading.
        """
        # Create a full-screen window and save dimensions
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

        pygame.display.set_caption("Alien Invasion")  # Set window title

        self.number_of_faraway_stars = randint(100, 200)  # Random star count for background

        self.bg_image_sources = self.create_image_sources()  # Prepare background assets

        self.bullets_allowed = 3               # Max player bullets on screen
        self.alien_bullets_allowed = 3         # Max alien bullets on screen

        self.alien_drop_speed = 20.0           # How far the fleet drops down
        self.fleet_direction = 1               # Fleet moves right (1) or left (-1)

        self.ship_limit = 3                    # Number of player lives

        self.speedup_scale = 1.1               # Rate at which game speeds up
        self.score_scale = 1.5                 # How quickly scoring increases

        self.bg_surface = BackGround(self).build()  # Build the background visual
        self.screen_manager = ScreenManager(self)   # Create screen manager

        self.initialize_dynamic_settings()     # Set initial dynamic settings

    def initialize_dynamic_settings(self):
        """
        Initializes values that change during gameplay.
        """
        self.ship_speed = 1.0
        self.alien_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_bullet_speed = 2.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """
        Speeds up game dynamics and increases scoring as difficulty rises.
        """
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        # Alien score also increases — convert to int to avoid fractional scores
        self.alien_points = int(self.alien_points * self.score_scale)

    def create_image_sources(self):
        """
        Creates a dictionary of galaxy image paths mapped to a random value.
        Returns:
            dict: Dictionary of image paths and their associated value.
        """
        images = {"galaxy": 9}
        result = {}
        for image, value in images.items():
            for n in range(1, value + 1):
                image_path = "images/%s_%d.png" % (image, n)
                result[image_path] = randint(0, 2)
        return result
