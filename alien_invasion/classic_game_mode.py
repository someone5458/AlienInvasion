import pygame
import sys

from random import choice
from time import sleep

from screen import Screen

from ship import Ship
from alien import Alien
from bullet import Bullet
from alien_bullet import AlienBullet
from game_stats import GameStats
from scoreboard import ScoreBoard
from button import Button
from bg_builder import BackGround
from start_pause_end import StartPauseEndButtons
from save_file import SaveFile

class ClassicGameMode(Screen):

    def __init__(self, manager, settings, menu):
        super().__init__(manager)

        self.settings = settings
        self.screen = settings.screen
        self.screen_rect = settings.screen_rect
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        
        self.menu = menu
        self.settings = settings
        
        self.save_file = SaveFile()
        self.stats = GameStats(self) # creating an instance for storing statistics
        self.bg_surface = BackGround(self.settings).build()
        self.ship = Ship(self) # ship instance
        self.sb = ScoreBoard(self) # score board instance
        self.spe = StartPauseEndButtons(ClassicGameMode, self)
        
        
        # creating sprite groups to manage them
        self.alien_bullets = pygame.sprite.Group() 
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.spe._update_mouse_visibility()
        self.spe._check_start()
        self._create_fleet()

        self.stats.games_played += 1


    def _check_event(self):
            """tracking keyboard and mouse events"""
            for event in pygame.event.get(): # returns a list of all events that have occurred since the last call. The loop iterates through each of them
                if event.type == pygame.QUIT:
                    self.save_file.save()
                    sys.exit(self.stats)
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.stats.game_active:
                    mouse_pos = pygame.mouse.get_pos()
                    self.spe._check_buttons_events(mouse_pos)

    
    def _update(self):
        if self.stats.game_active:    
            self.ship.update()
            self._update_bullets()
            self._update_alien_bullets()
            self._update_aliens()
    

    def _update_screen(self):
        self.screen.blit(self.bg_surface, (0, 0)) # draws the background image
        #self.screen.fill(self.bg_color) # fills the window with the selected color
        #self.stars.draw(self.screen) # The draw() method is called, which draws each star from the sprite group.
        self.ship.blitme() # a ship class method that draws a ship
        
        # showing other game objects
        self.bullets.draw(self.screen)
        self.alien_bullets.draw(self.screen)
        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            for button in self.spe.active_buttons:
                button.draw_button()
    
        pygame.display.flip()


    def _check_keydown_events(self, event):
        """registers keystrokes and responds to them"""   
        if event.key == pygame.K_ESCAPE:
            self.save_file.save(self.stats)
            sys.exit()
        # While holding down the A and D keys, the ship's flags, which are responsible for moving left and right, change.
        if event.key == pygame.K_d: 
            self.ship.moving_right = True
        if event.key == pygame.K_a:
            self.ship.moving_left = True
        
        if event.key == pygame.K_q:
            self.spe._check_pause()
        if event.key == pygame.K_SPACE: # the ship fires when the space bar is pressed
            self._fire_bullet()
    

    def _check_keyup_events(self, event):
        """registers key releases and responds to them"""       
        # When the corresponding keys are released, the ship's flags change and movement stops.
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        if event.key == pygame.K_a: 
            self.ship.moving_left = False


    def _create_fleet(self):
        """creates a fleet of alien ships"""
        alien = Alien(self) 
        alien_width, alien_height = alien.rect.size # The size attribute stores a tuple of width and height. They are saved in separate variables.
        
        # calculations to determine the available space along the x and y axes, as well as the number of alien ships that can fit in it
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_columns = available_space_x // (2 * alien_width)
        available_space_y = self.settings.screen_height - (3 * alien_height) - self.ship.rect.height # aliens should not appear in the ship's area
        number_rows = available_space_y // (3 * alien_height)

        # For each position in the row and column, an instance of an alien is created and added to the general group of aliens.
        for row in range(number_rows):
            for column in range(number_columns):
                self._create_alien(column, row)


    def _create_alien(self, column, row):
        """creates an instance of an alien, assigns coordinates to it, and adds it to the group of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        alien.x = alien_width + 2 * alien_width * column # calculation of the exact coordinates of the alien
        alien.rect.x = alien.x # the coordinate is passed to alien.rect.x so that the sprite is drawn in the correct place on the screen
        
        alien.rect.y = alien_height + 2 * alien.rect.height * row
        self.aliens.add(alien) # after calculating the coordinates, the alien instance is added to the group


    def _fire_bullet(self):
        """fires a shot from the ship. A shot can only be fired if the number of bullets already fired is less than the maximum number allowed."""
        if len(self.bullets) < self.settings.bullets_allowed: # comparison of the number of bullets in a group with the maximum number of bullets
            
            # A new instance of the bullet is created and added to the group.
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    

    def _fire_alien_bullet(self, alien):
        """
        fires a shot from the alien. The maximum number of bullets available 
        depends on the number of remaining aliens. The fewer aliens there are, 
        the lower the maximum number of bullets.
        """
        # calculating the maximum number of bullets, it will never be higher than the number of remaining aliens
        alien_bullets_allowed = min(self.settings.alien_bullets_allowed, len(self.aliens))
        
        if len(self.alien_bullets) < alien_bullets_allowed:
            new_alien_bullet = AlienBullet(self, alien)
            self.alien_bullets.add(new_alien_bullet)


    def _update_bullets(self):
        """updates the position of the bullet and also removes it from the group if it flies off the edge of the screen"""
        self.bullets.update() # calls the bullet class method, which launches it upward
        
        # A loop is created for each bullet in the group copy. Since bullet instances should not be deleted from the actual group in the loop.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= self.screen_rect.top:
                self.bullets.remove(bullet) # removes bullets that have flown off the screen

        self._check_bullet_alien_collisions() # checking bullet collisions with the alien


    def _check_bullet_alien_collisions(self):
        """checking whether the bullet hit the alien"""
        # pygame.sprite.groupcollide() checks for collisions between elements of two groups. 
        # The groups are specified in the method brackets. Two True arguments indicate that 
        # both colliding objects should be deleted. If you specify “False, True”, the bullet 
        # will “delete” every alien in its path and continue flying.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True) # A dictionary where the keys are bullets that hit the alien, and the values are a list of aliens that were destroyed by that bullet.
         
        # checks whether the group of newcomers is empty. If the group is empty, the level is reset and a new fleet is created.
        if not self.aliens:
            self._increase_level()

        # checking whether the collision dictionary is not empty. (Did the bullet hit the alien?)
        if collisions:
            self._update_score(collisions)


    def _increase_level(self):
        """After destroying the last alien from the fleet, a group of bullets is cleared, the game speed increases, and a new fleet is created."""
        self.bullets.empty() # removes all bullets from the group
        
        self.settings.increase_speed()
        self._create_fleet()
        self.sb.check_level()


    def _update_score(self, collisions):
        """updates the score, redraws the scoreboard, checks the high score"""
        # A loop is created that iterates through all aliens in the returned dictionary to correctly calculate the number of points.
        for aliens in collisions.values():
            # The cost of each alien is multiplied by the number of aliens on the list, and the result is added to the current score.
            self.stats.score += self.settings.alien_points * len(aliens)
            
        # Next, using the methods of the scoreboard class, its image is updated.
        self.sb.prep_score()
        self.sb.check_high_score()
        self.stats.aliens_destroyed += 1
        self.save_file._update_data(self.stats)


    def _update_alien_bullets(self):
        """updates the position of the alien bullet and also removes it from the group if it flies off the edge of the screen"""
        self.alien_bullets.update() # calls the bullet class method, which launches it upward
        
        # checking the position of bullets, removing bullets if it has flown off the screen
        for alien_bullet in self.alien_bullets.copy(): 
            if alien_bullet.rect.top >= self.screen_rect.bottom:
                self.alien_bullets.remove(alien_bullet)
        
        # checking the collision of the alien's bullet with the ship
        self._check_alien_bullet_ship_collitions()


    def _check_alien_bullet_ship_collitions(self):
        """Checks for collision between the alien's bullet and the ship. If there is a collision, the ship is destroyed."""
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit() # registration of hits on the ship and processing of this


    def _ship_hit(self):
        """
        Checks the number of remaining ships.
        If it is greater than zero, restarts the current level.
        If the number drops to zero, the active pause of the game 
        ends and the mouse cursor becomes visible.
        """
        # checking the number of remaining ships
        if self.stats.ships_left > 0:
            self._restart_after_hit()
        else:
            self.save_file.save(self.stats)
            self.spe._check_end()


    def _restart_after_hit(self):
        """
        decreases the number of ships by 1, updates the table, clears 
        the alien groups and all bullets, moves the ship to its initial 
        position, and pauses the game for 0.5 seconds.
        """
        # decreases the number of ships by 1.
        self.stats.ships_left -= 1
        self.sb.prep_ships()
        
        # clears the alien groups and all bullets.
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        
        self._create_fleet()
        self.ship.center_ship() # moves the ship to the center of the screen.

        self.stats.ships_lost += 1
        self.save_file._update_data(self.stats)

        sleep(0.5) # pausing the game for 0.5 seconds   


    def _update_aliens(self):
        """
        checks whether the alien has collided with the ship or 
        reached the bottom edge of the screen, selects the aliens 
        that will fire, updates the position of the entire fleet
        """
        self._check_fleet_edges() # checks whether the fleet has reached the edge of the screen

        # checks for collisions between the ship and aliens from the fleet The spritecollideany() 
        # method takes two arguments: a sprite and a group. The method attempts to find any element 
        # of the group that collides with the sprite. The method returns the first element of the 
        # group that collides with the sprite. 
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom() # checks whether any alien has reached the bottom edge of the screen
        self._fire_alien_bullet(choice(list(self.aliens))) # A random alien is selected from the group to shoot.

        self.aliens.update() # Updates the position of each alien in the group. Calls the update() method for each member of the group.


    def _check_fleet_edges(self):
        """checks whether the alien from the fleet has reached the edge of the screen"""
        for alien in self.aliens.sprites():
            # For each alien in the group, check the return value of its class method.
            # When one of the aliens reaches the edge, the direction of movement 
            # changes to the opposite with a slight decrease in the fleet. 
            if alien.check_edges():
                self._change_fleet_direction()
                break # the cycle ends with the first alien found

    
    def _change_fleet_direction(self):
        """lowers the fleet and changes its direction"""
        for alien in self.aliens.sprites(): # Each alien from the group descends to a certain distance.
            alien.rect.y += self.settings.alien_drop_speed

        # The direction value from the settings is multiplied by -1 so that it changes to the opposite. 
        # The command is not added to the cycle, as the direction of movement should only change once.
        self.settings.fleet_direction *= -1


    def _check_aliens_bottom(self):
        """check whether the alien has reached the bottom edge of the screen; if so, it counts as a hit on the ship"""
        for alien in self.aliens.sprites():
            
            # If the bottom edge of the alien reaches the bottom edge of the screen, the same thing happens as when it collides with the ship.
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_hit()
                break






























