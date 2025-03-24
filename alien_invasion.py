import sys
import pygame

from random import randint, choice
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
from alien_bullet import AlienBullet

class AlienInvasion():
    """класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """инициирует игровой процесс и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.screen_rect = self.screen.get_rect()
        self.bg_color = (self.settings.bg_color)
        
        #создание экземпляра для хранения статистики
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.sb = ScoreBoard(self)
        
        self.alien_bullets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_starry_sky()

        #создание экземпляра кнопки игры. Помимо экземпляра игры, ему передается строка с надписью, которая будет на кнопке
        self.play_button = Button(self, "Play")

    def run_game(self):
        """запуск основного цикла игры"""
        while True:
            #функция должна выполнятся всегда, так как программа должна считывать действия пользователя
            self._check_ivents()
            #функции выполняются только в активной фазе, тоесть до того как игрок потеряет все три корабля
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien_bullets()
                self._update_aliens()
            #экран должен обновляться также и в неактивной фазе
            self._update_screen()
    
    def _check_ivents(self):
        """отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #позиция курсора мыши сохраняется в переменной.
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    #непрерывное движение вправо и влево
    def _check_keydown_events(self, event):
        """отслкживает нажатие клавиш и реагирует на это"""   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.ship.moving_right = True
            if event.key == pygame.K_a:
                self.ship.moving_left = True
            if event.key == pygame.K_q:
                sys.exit()
            if event.key == pygame.K_SPACE:
                self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """отслеживает отпускание клавиш и реагирует на это"""       
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.ship.moving_right = False
            if event.key == pygame.K_a: 
                self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.new_bullet = Bullet(self)
            self.bullets.add(self.new_bullet)
    
    def _fire_alien_bullet(self, alien):
        alien_bullets_allowed = self.settings.alien_bullets_allowed % len(self.aliens)
        if len(self.alien_bullets) < alien_bullets_allowed:
            self.new_alien_bullet = AlienBullet(self, alien)
            self.alien_bullets.add(self.new_alien_bullet)

    def _update_screen(self):
        #при кожному проході циклу перемальовується екран
        self.screen.fill(self.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.create_bullet()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.show_alien_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        #кнопка появляется только в неактивной фазе игры, поэтому создается условие
        if not self.stats.game_active:
            self.play_button.draw_button()
        #відображення останнього промальованого екрана
        pygame.display.flip()
    
    def _check_play_button(self, mouse_pos):
        """запускает игру по щелчку мыши по кнопке"""
        #в переменной сохраняется значение True или False. Метод collidepoint() используется
        # для проверки того, находится ли точка щелчка (mouse_pos) в пределах области, определяемой прямоугольником кнопки Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #условие срабатывает только когда пользователь нажимает на кнопку во время неактивной фазы игры. 
        #Так как без этого на кнопку можно нажать и в активной фазе
        if button_clicked and not self.stats.game_active:
            #сброс игры
            #количество оставшихся кораблей обновляется. начинается активная фаза игры 
            self.stats.reset_stats()
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()
            
            self._create_fleet()
            self.ship.center_ship()

            #при нажатии кнопки игры счет и уровень сбрасываются. тоесть становятся такими какими были по умолчанию
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #после нажатия кнопки игры курсор мыши скрывается
            pygame.mouse.set_visible(False)

    def _ship_hit(self):
        """обрабатывает столконовение корабля"""
        if self.stats.ships_left > 0:
            #уменьшает количество кораблей на 1
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #очищает группы пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            #создвет новый флот
            self._create_fleet()
            #перемещает корабль на центр экрана
            self.ship.center_ship()
            #приостанавливает программу на 0.5 сек
            sleep(0.5)

        else:
            self.stats.game_active = False
            #делает курсор мыши видимым
            pygame.mouse.set_visible(True)

    def _update_bullets(self):
        """обновляет позицию снаряда"""
        #вызывает метод класса снаряда, который запускет его вверх
        self.bullets.update()     
        
        #удаляет снаряды, которые вылетели за пределы экрана
        #создается цикл для каждого снаряда в копии группы. так как экземпляры не должны удаляться из настоящей группы в цикле
        for bullet in self.bullets.copy():
            #если снаряд перелетел верх экрана то он удаляется из группы
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        self.alien_bullets.update()
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.screen_rect.bottom:
                self.alien_bullets.remove(alien_bullet)
        self._check_alien_bullet_ship_collitions()

    def _check_bullet_alien_collisions(self):
        """проверка попадания снаряда в пришельца:"""
        #вызывается метод pygame.sprite.groupcollide(). Он проверяет колизии между элементами двух групп.
        #Эти группы уазываются в скобках метода. Каждый раз когда хитбокс снаряда и пришельца пересекаются,
        #метод добавляет пару снаряда и пришельца в возвращаемый словарь. Два аргумента True сообщают, что
        #нужно удалить оба столкнувшиеся объекты. Если указать "False, True", то снаряд будет "удалять" каждого 
        #пришельца на своем пути, а сам будет лететь дальше
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        #проверяет группу на наличие элементов (пришельцев). Если группа пуста то вызывает метод empty() для группы
        #снарядов, который удаляет все эелементы(снаряды) из группы. Далее вызывается метод, создающий новый флот. и игра продолжается  
        if not self.aliens:
            self.bullets.empty()
            #после уничтожения последнего пришельца из флота увеличивается скорость игры и создается новый флот
            self.settings.increase_speed()
            self._create_fleet()
            self.sb.check_level()
        
        #проверяется колизия снаряда и пришельца
        if collisions:
            #создается цикл, который перебирает всех пришельцев в возвращаемом словаре для корректного подсчета количества очков
            for aliens in collisions.values():
                #Стоимость каждого пришельца умножается на количество пришельцев в списке, а результат прибавляется к текущему счету  
                self.stats.score += self.settings.alien_points * len(aliens)
                #далее вызывается метод класса таблицы очков, который создает новое изображение текущего счета
            self.sb.prep_score()
            self.sb.check_hight_score()
        
    def _check_alien_bullet_ship_collitions(self):
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        available_space_y = self.settings.screen_height - (3 * alien_height) - self.ship.rect.height
        number_rows = available_space_y // (3 * alien_height)

        for row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row)
                
    def _create_alien(self, alien_number, row):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row
        self.aliens.add(alien)
    
    def _update_aliens(self):
        """обновляет позицию флота"""
        #проверяет долетел ли флот до края экрана
        self._check_fleet_edges()

        #проверяет столкновене корабля и пришельца из флота
        #функция spritecollideany получает два аргумента: спрайт и группу. функция пытается найти любой элемент группы
        #столкнувшийся со спрайтом. когда это происходит функция возвращает первый элемент группы столкнувшийся со спрайтом.
        #при столкновении выполняется условие и выводится надпись что корабль поражен   
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #проверяет достиг ли какой то пришелец нижнего края экрана
        self._check_aliens_bottom()
        
        self._fire_alien_bullet(choice(list(self.aliens)))

        #обновляет позицию каждого пришельца в группе. Для каждого из группы вызывает метод update()
        self.aliens.update()


    def _check_fleet_edges(self):
        """проверяет достиг ли пришелец из флота края экрана"""
        #создается цикл для каждого пришельца в группе
        for alien in self.aliens.sprites():
            #проверяет возвращаемое значение метода класса пришельца. 
            #при достижении края одним из пришельцев условие выполняется и направление
            #движения меняется на противоположное с небольшим снижением флота 
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """метод проверят достиг ли пришелец нижнего края экрана"""
        #цикл перебирает всех пришельцев в группе
        for alien in self.aliens.sprites():
            #создается условие: если нижний край пришельца достиг нижнего края экрана, происходит то же самое что и при столкновении с кораблем
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """снижает флот и меняет напрвление движения"""
        #цикл для каждого пришельца в группе
        for alien in self.aliens.sprites():
            #к координате у хитбокса пришельца добавляется величина из настроек, за счет его флот снижается 
            alien.rect.y += self.settings.alien_drop_speed

        #значение направления из настроек умножается на -1, что бы оно поменялось на противоположное
        #команда не добавляется в цикл, так как напревление движения должно смениться всего один раз
        self.settings.fleet_direction *= -1

    def _create_starry_sky(self):
        """создает звездное небо"""
        #максимальное коичество звезд
        star_number = 60
        #цикл для создания звезд в заданном количестве
        for star in range(star_number):
            self._create_star()

    def _create_star(self):
        """метод создает звезду для построения рядов"""
        star = Star(self)
        #создание 2 рандомных чисел для координат звезды
        random_cord_x = randint(self.screen_rect.left, self.screen_rect.right)
        random_cord_y = randint(self.screen_rect.top, self.screen_rect.bottom)
        #назначение координат звезды
        star.rect.x = random_cord_x
        star.rect.y = random_cord_y
        #экземпляр звезды с собственной позицией добавляется в группу
        self.stars.add(star)

if __name__ == '__main__':
    #створення екземпляру та запуск гри
    ai = AlienInvasion()
    ai.run_game()
