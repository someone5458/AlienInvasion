import pygame
from pygame.sprite import Sprite
from alien import Alien

class AlienBullet(Sprite):
    def __init__(self, ai_game, alien):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings
        self.alien = alien

        self.image = pygame.image.load("images/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.midtop = self.alien.rect.midbottom

        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y
    
    def show_alien_bullet(self):
        self.screen.blit(self.image, self.rect)