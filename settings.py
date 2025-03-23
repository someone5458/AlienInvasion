class Settings():

    def __init__(self):
        self.screen_width = 0
        self.screen_height = 0
        self.bg_color = (10, 10, 90)
        
        self.bullets_allowed = 3

        self.alien_bullets_allowed = 2

        #скорость снижения флота
        self.alien_drop_speed = 20.0

        #настройки корабля
        self.ship_limit = 3
        
        #fleet_direction означает направление движения флота. 1 - вправо. -1 - влево.
        self.fleet_direction = 1

        #в переменной сохранен прирост скорости игры
        self.speedup_scale = 1.1

        #множитель очков
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed = 1.0
        self.alien_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_bullet_speed = 2.0

        self.fleet_direction = 1

        self.alien_points = 50
    
    def increase_speed(self):
        """увеличивает настройки скорости"""
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        #После увеличения скорости игры стоимость каждого попадания также увеличивается.
        #Чтобы счет возрастал на целое количество очков, используется функция int()
        self.alien_points = int(self.alien_points * self.score_scale)

