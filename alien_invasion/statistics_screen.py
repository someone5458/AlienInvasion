import pygame
import sys

from screen import Screen
from button import Button
from save_file import SaveFile

class Statistics(Screen):
    """
    A screen that displays saved game statistics, such as high scores or other tracked metrics.
    """

    def __init__(self, menu, manager, settings):
        """
        Initialize the statistics screen with references to the main menu, game manager, and settings.

        Args:
            menu: The main menu screen to return to.
            manager: The screen manager handling screen transitions.
            settings: Game settings, including screen dimensions and background surface.
        """
        super().__init__(manager)
        
        self.settings = settings
        self.screen = settings.screen
        self.screen_rect = settings.screen_rect
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height
        self.bg_surface = settings.bg_surface

        self.menu = menu

        self.save = SaveFile()
        self.save_categories = self.save._load_data()  # Load saved statistics
        self.category_items = {}  # Stores rendered category images and their positions

        self.buttons_msgs = [
            "return"
        ]

        self._create_frame()
        self._create_categories()
        self.buttons = self._create_buttons()
    
    def _create_buttons(self):
        """
        Create and return a list of buttons for the statistics screen.

        Returns:
            list: A list of Button instances positioned vertically below the stats frame.
        """
        buttons = []
        offset = 50
        start_pos = (self.screen_rect.centerx, self.frame_rect.bottom)
        for button_msg in self.buttons_msgs:
            new_button = Button(self, button_msg, position=start_pos, offset_y=offset)
            offset += new_button.rect.height * 1.5  # Vertical spacing between buttons
            buttons.append(new_button)
        return buttons
    
    def _check_event(self):
        """
        Process events such as window closing, ESC key press, or mouse clicks.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)

    def _check_buttons(self, click_pos):
        """
        Check if any button was clicked and handle its action.

        Args:
            click_pos (tuple): The mouse click position.
        """
        for button in self.buttons:
            if button.rect.collidepoint(click_pos):
                if button.message == "return":
                    self.manager.switch_screen(self.menu)

    def _update_screen(self):
        """
        Render the background, stats frame, category items, and buttons, then update the display.
        """
        self.screen.blit(self.bg_surface, (0, 0))
        self._draw_frame()
        for button in self.buttons:
            button.draw_button()
        pygame.display.flip()
    
    def _create_frame(self):
        """
        Define the frame area where statistics will be displayed.
        """
        self.frame_color = (35, 30, 30)
        self.frame_rect = pygame.Rect(0, 0, 500, 400)
        self.frame_rect.center = self.screen_rect.center

    def _prep_category(self, category, value, offset_y=0):
        """
        Prepare a single category's image and position for rendering.

        Args:
            category (str): The name of the statistic.
            value (int): The value associated with the statistic.
            offset_y (int): Vertical offset index.

        Returns:
            tuple: A rendered image and its rectangle.
        """
        text_color = (255, 255, 255)
        font = pygame.font.SysFont(None, 48)

        category_str = f"{category}: " + "{:,}".format(value)
        category_image = font.render(category_str, False, text_color)
        category_rect = category_image.get_rect()

        category_rect.top = self.frame_rect.top + (category_rect.height * 1.5) * offset_y
        category_rect.centerx = self.frame_rect.centerx

        return category_image, category_rect

    def _create_categories(self):
        """
        Generate and prepare rendered statistics to be displayed inside the frame.
        """
        sample_image, sample_rect = self._prep_category("a", 0)  # Example to calculate spacing
        available_space_y = self.frame_rect.height - sample_rect.height * 2
        number_of_categories = min(available_space_y // (sample_rect.height * 2), len(self.save_categories))

        # Format category names (capitalize and replace underscores)
        categories = [
            (key.title().replace("_", " "), value)
            for key, value in self.save_categories.items()
        ]
        
        for n in range(1, number_of_categories + 1):
            category, value = categories[n - 1]
            category_image, category_rect = self._prep_category(category, value, offset_y=n)
            self.category_items[category_image] = category_rect

    def _draw_frame(self):
        """
        Draw the stats frame and all category items inside it.
        """
        self.screen.fill(self.frame_color, self.frame_rect)
        for category_image, category_rect in self.category_items.items():
            self.screen.blit(category_image, category_rect)
