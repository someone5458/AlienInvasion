import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """класс для звезды"""
    def __init__(self, ai_game):
        """создание атрибутов звезды"""
        super().__init__()

        #получает основной экран игры 
        self.screen = ai_game.screen

        #загружает изображение звезды и создает хитбокс для него
        self.image = pygame.image.load("images/star.png")
        self.rect = self.image.get_rect()

        #определяет координаты звезды
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)