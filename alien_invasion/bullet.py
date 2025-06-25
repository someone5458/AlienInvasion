import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """class for managing player resources and behavior"""
    
    def __init__(self, ai_game):
        """initialization of the main attributes of the class"""
        super().__init__() # Calls the constructor of the Sprite base class.
        
        self.screen = ai_game.screen # link to the game screen
        self.screen_rect = self.screen.get_rect() # creating a rectangle for the screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("images/bullet.png") # loading the bullet image
        self.rect = self.image.get_rect() # creating the bullet hitbox
        
        self.rect.midtop = ai_game.ship.rect.midtop # initial position of the bullet. always in front of the bow of the ship

        self.y = float(self.rect.y) # Saves the exact vertical position of the bullet as a floating point number.
    

    def update(self):
        """updates the bullet's position and launches it upward"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    