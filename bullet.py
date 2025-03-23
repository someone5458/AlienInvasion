import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        self.settings = ai_game.settings

        self.image = pygame.image.load("images/one_shot.png")
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)
    
    def update(self):
        self.y -= self.settings.bullet_speed

        self.rect.y = self.y
    
    def create_bullet(self):
        self.screen.blit(self.image, self.rect)