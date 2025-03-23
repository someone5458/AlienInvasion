import pygame.font

from ship import Ship
from pygame.sprite import Group

class ScoreBoard():
    """класс для вывода игровой информации"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        #подготовка изображений счетов
        self.prep_score()
        self.prep_hight_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """преобразует текущий счет в графическое изображение"""
        #округляет счет до десятков и сохраняет его в rounded_score
        #функция round() округляет значение, переданное в первом аргументе до заданого количества знаков во втором аргументе
        #если передается отрицательное число то функция округляет число до ближайшего десятка, сотни, тысячи и тд.  
        rounded_score = round(self.stats.score, -1)
        #далее директива форматирования строки приказывает Python вставить запятые при преобразовании числового значения в строку
        #— например, чтобы вместо 1000000 выводилась строка 1,000,000
        self.score_str = "score:" + "{:,}".format(rounded_score)
        #получение счета и создание изображения текста
        self.score_image = self.font.render(self.score_str, False, self.text_color, self.settings.bg_color)

        #создание хитбокса изображения текста и назначение его позиции. справа сверху
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = self.screen_rect.top
        self.score_rect.right = self.screen_rect.right - 20
    
    def prep_hight_score(self):
        rounded_hight_score = round(self.stats.hight_score, -1)
        self.hight_score_str = "Hight score:" + "{:,}".format(rounded_hight_score)
        
        self.hight_score_image = self.font.render(self.hight_score_str, False, self.text_color, self.settings.bg_color)
        self.hight_score_rect = self.hight_score_image.get_rect()
        
        self.hight_score_rect.centerx = self.screen_rect.centerx
        self.hight_score_rect.top = self.screen_rect.top

    def show_score(self):
        """отображает изображение счета на экране"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hight_score_image, self.hight_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    
    def check_hight_score(self):
        """обновляет рекор набраных очков"""
        #если текущее количество очков больше рекордного, то рекордные приравниваются к текущим и обновляется изображение счета
        if self.stats.score > self.stats.hight_score:
            self.stats.hight_score = self.stats.score
            self.prep_hight_score()
    
    def prep_level(self):
        """преобразует уровень в графическое изображение"""
        self.level_str = "Level:" + str(self.stats.level)
        self.level_image = self.font.render(self.level_str, False, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        
        self.level_rect.top = self.score_rect.bottom + 20
        self.level_rect.right = self.score_rect.right
    
    def check_level(self):
        self.stats.level += 1
        self.prep_level()
        
    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)