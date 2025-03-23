import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Класс для управления кораблем."""
    def __init__(self, ai):
        """Инициализирует корабль и задает его начальную позицию."""
        #наследует от класса Sprite
        super().__init__()
        self.screen = ai.screen
        self.screen_rect = ai.screen.get_rect()
    
        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom
        #флаг перемещения
        self.moving_right = False
        self.moving_left = False

        self.settings = ai.settings 
        self.x = float(self.rect.x)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
    
    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """размещает корабль в центре нижней стороны"""
        #выравнивает корабль по центру
        self.rect.midbottom = self.screen_rect.midbottom
        #после выравнивания сбрасывается атрибут self.x, что бы в программе отслеживалась точная позиция корабля
        self.x = float(self.rect.x)