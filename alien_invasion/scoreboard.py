import pygame.font
from ship import Ship
from pygame.sprite import Group

class ScoreBoard():
    """class for displaying game information"""
    
    def __init__(self, game):
        """initialization of the main attributes of the class"""
        
        # Main links to gaming resources
        self.ai_game = game
        self.screen = game.screen
        self.settings = game.settings
        self.stats = game.stats
        
        self.screen_rect = self.screen.get_rect() # creating a rectangle for the screen
        
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) # Prepare the attribute for text output.
        
        # preparing images on the scoreboard
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """converts the current score into a graphical representation"""
        # Rounds the score to the nearest ten and saves it in rounded_score. 
        # The round() function rounds the value passed in the first argument 
        # to the number of digits specified in the second argument. If a 
        # negative number is passed, the function rounds the number to the 
        # nearest ten, hundred, thousand, etc.
        rounded_score = round(self.stats.score, -1)
        
        self.score_str = "score:" + "{:,}".format(rounded_score) # inserting commas when converting a numeric value to a string
        self.score_image = self.font.render(self.score_str, False, self.text_color) # obtaining score and creating text image

        # Creating a rectangle for the text image and assigning its position. Top right
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = self.screen_rect.top
        self.score_rect.right = self.screen_rect.right - 20
    

    def prep_high_score(self):
        """converts the current hight score into a graphical representation"""
        rounded_high_score = round(self.stats.high_score, -1)
        self.high_score_str = "Hight score:" + "{:,}".format(rounded_high_score)
        
        self.high_score_image = self.font.render(self.high_score_str, False, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        
        # placement of an record high image score at the top of the center
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top


    def prep_level(self):
        """converts the level value into a graphical image"""
        self.level_str = "Level:" + str(self.stats.level)
        self.level_image = self.font.render(self.level_str, False, self.text_color)
        self.level_rect = self.level_image.get_rect()
        
        # placement of the level image to the right below the score image
        self.level_rect.top = self.score_rect.bottom + 20
        self.level_rect.right = self.score_rect.right
    
    
    def prep_ships(self):
        """shows the number of remaining ships"""
        self.ships = Group() # creating a group of ships for display
        
        for ship_number in range(self.stats.ships_left):
            # creating a ship instance and assigning its coordinates in the upper left row
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship) # each ship is added to the group


    def show_score(self):
        """displays the entire table of points, level, number of remaining ships on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    

    def check_high_score(self):
        """updates the score record"""
        #if the current score is higher than the high score, then the high scores are equated to the current scores
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score() # the image of the highest score is updated


    def check_level(self):
        """raises the level and updates its image"""
        self.stats.level += 1
        self.prep_level()
    


