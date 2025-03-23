import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("images/alien_ship.png")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
    
    def check_edges(self):
        """возвращает True если пришелец находится у края экрана. Вызов метода позволяет проверить достиг ли пришелец края экрана"""
        #создает прямоугольник для экрана
        self.screen_rect = self.screen.get_rect()
        #возвращает True только в момент когда пришелец достигает правого края экрана или левого края. В остальное время не возвращает True
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """обновляет позицию пришельца"""
        #к координате х пришельца добавляет число скорости пришельца и умножает на число направления движения (1 или -1). 
        # Тоесть если оно будет -1 то от координаты х будет отниматься число скорости и пришелец будет двигаться влево.
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    

    