import pygame
from random import randint, choice

class BackgroundObjectLayer:
    """
    Represents a visual layer composed of multiple randomly placed instances of a given image.
    These can be used to simulate visual elements like stars, clouds, or nebulas in a game background.
    """

    def __init__(self, image_path, count, screen_size, offset=(0, 0), paint=False, transparency=255):
        """
        Initializes the BackgroundObjectLayer with given parameters.

        Args:
            image_path (str): Path to the image file to be used in the layer.
            count (int): Number of image instances to generate.
            screen_size (tuple): Size of the screen (width, height).
            offset (tuple): Optional offset to shift image positions (x, y).
            paint (bool): Whether to apply a random tint color to each image.
            transparency (int): Alpha transparency value (0-255) for painted images.
        """
        # Load the base image with transparency
        self.image = pygame.image.load(image_path).convert_alpha()

        self.count = count
        self.screen_size = screen_size
        self.screen_width, self.screen_height = screen_size
        self.paint = paint
        self.transparency = transparency

        # Apply offset values with optional direction randomization
        self.offset_x, self.offset_y = offset
        self.offset_x = -self.offset_x if choice([True, False]) else self.offset_x
        self.offset_y = -self.offset_y if choice([True, False]) else self.offset_y

        # Randomly place 'count' number of image rectangles across the screen
        self.rects = []
        for _ in range(self.count):
            rect = self.image.get_rect()
            rect.x = randint(0, self.screen_width)
            rect.y = randint(0, self.screen_height)
            self.rects.append(rect)

        # Available tint colors for painting (used if paint=True)
        self.tint_colors = [(220, 0, 255), (255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 120, 255)]

    def draw(self, surface):
        """
        Draws each image instance on the provided surface with optional rotation and tinting.

        Args:
            surface (pygame.Surface): The target surface to draw onto.
        """
        for rect in self.rects:
            rotated_image = pygame.transform.rotate(self.image, randint(0, 360))
            draw_rect = rect.copy()
            draw_rect.x += self.offset_x
            draw_rect.y += self.offset_y

            if self.paint:
                tint_color = choice(self.tint_colors)
                rotated_image = tint_image(rotated_image, tint_color)
                rotated_image.set_alpha(self.transparency)

            surface.blit(rotated_image, draw_rect)

    def draw_nebulas(self, surface):
        """
        Draws larger, more transparent and tinted versions of the image to simulate nebulas.

        Args:
            surface (pygame.Surface): The target surface to draw onto.
        """
        for rect in self.rects:
            rotated_image = pygame.transform.rotate(self.image, randint(0, 360))
            tint_color = choice(self.tint_colors)
            rotated_image = tint_image(rotated_image, tint_color)
            rotated_image.set_alpha(min(randint(50, 120), 150))  # Softer transparency for nebula effect

            # Scale up the image to make it appear more diffused
            rotated_image = pygame.transform.scale_by(rotated_image, randint(2, 3))

            draw_rect = rect.copy()
            draw_rect.x += self.offset_x
            draw_rect.y += self.offset_y
            surface.blit(rotated_image, draw_rect)


def tint_image(image, tint_color):
    """
    Tints the given image by blending it with a solid color while preserving transparency.

    Args:
        image (pygame.Surface): The image to tint.
        tint_color (tuple): RGB tuple specifying the tint color.

    Returns:
        pygame.Surface: The tinted image surface.
    """
    tinted_image = image.copy()
    tint_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    tint_surface.fill(tint_color)
    tinted_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted_image