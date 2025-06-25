import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Class for ship management"""
    
    def __init__(self, game):
        """initialization of the main attributes of the class"""
        super().__init__() # Calls the constructor of the Sprite base class.
        
        self.screen = game.screen # link to the game
        self.screen_rect = game.screen.get_rect() # link to the screen rectangle
        self.settings = game.settings 
        
        self.image = pygame.image.load('images/ship.png') # loading the ship image
        self.rect = self.image.get_rect() # creating the ship's hitbox
        self.rect.midbottom = self.screen_rect.midbottom # setting the initial position at the center of the bottom edge of the screen
        
        # movement flags
        self.moving_right = False
        self.moving_left = False

        self.x = float(self.rect.x) # Saves the exact horizontal position of the ship as a floating point number.


    def update(self):
        """
        Updates the ship's position, moves it left and right if the corresponding 
        flag is active. Prevents the ship from flying off the screen.
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        self.rect.x = self.x # Synchronizes the exact position of the ship with its hitbox
    

    def blitme(self):
        """Draws an image of the ship at the current position of its hitbox."""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """places the ship in the center at the bottom edge of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom # aligning the ship in the center
        self.x = float(self.rect.x) # Synchronizes self.x with the new value of rect.x for smooth movement