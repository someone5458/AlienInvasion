import pygame.font # module that allows text to be displayed on the screen

class Button():
    """button creation class"""

    def __init__(self, game, msg, position=(0, 0), offset_x=0, offset_y=0):
        """initializes button attributes"""
        
        self.screen = game.screen # link to the game screen
        self.screen_rect = game.screen_rect # link to the rectangle of the screen
        
        self.message = msg # msg(message) - string with text on the button
        
        self.image = pygame.image.load("images/button.png")
        # Creates a rect object for the button, then aligns it to the center of the screen.
        self.rect = self.image.get_rect()
        
        self.rect.center = position
        self.rect.x += offset_x
        self.rect.y += offset_y      
        
        # Prepare the attribute for text output. None means the default font will be used, 48 means the text size.
        self.font = pygame.font.SysFont(None, 48) 
        self.text_color = (255, 255, 255)

        self.prep_msg(self.message) # pygame displays a string as a graphic image. The method is passed a variable with the button text.

    def prep_msg(self, msg):
        """converts text into an image, creates a rectangle, and aligns it in the center"""
        
        # An attribute is created that will store the rectangular image of the text. 
        # For the self.font attribute, the render() method is called, which creates 
        # the text image. It needs to be passed a variable with the button text, a 
        # logical indicator of the text smoothing mode (True) (letters will be 
        # smooth or pixelated), the font color, and the background color for this 
        # image (the button's own color will be used for the background, so that 
        # only the text is visually visible. If the background color is not specified, 
        # pygame attempts to display the text with a transparent background).
        self.msg_image = self.font.render(msg, False, self.text_color)

        # create a text rectangle and align it in the center of the button
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """draws the button frame and the text image on it"""
        # The fill() method draws the rectangular part of the button. The blit() method
        # displays the text image on the screen by transferring the image and the 
        # rectangle object. Two different methods are used because in the first case we 
        # fill the button rectangle with color, and in the second case we display the 
        # image with text on the screen.
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)