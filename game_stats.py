import pygame

class GameStats():
    """отслеживание статистики для игры"""

    def __init__(self, ai_game):
        """инициализирует статистику и получает настройки игры"""

        self.settings = ai_game.settings
        
        self.game_active = False
        
        self.hight_score = 0

        self.reset_stats()


    def reset_stats(self):
        """инициализирует статистику изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit

        #инициализирует настройки, изменяющиеся в ходе игры
        self.settings.initialize_dynamic_settings()

        #обнуляет счет
        self.score = 0

        #уровень инициуриется в этой функции, что бы он сбрасывался в начале каждой игры
        self.level = 1


