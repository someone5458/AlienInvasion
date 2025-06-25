import pygame
from background_object import BackgroundObjectLayer
from random import randint, choice

class BackGround:
    """Class for creating a space-themed background with stars, galaxies, and nebulas."""

    def __init__(self, settings):
        """
        Initialize the BackGround object with screen settings and load background layers.

        Args:
            settings: A settings object that contains screen size and image resource information.
        """
        # Save settings and extract screen dimensions
        self.settings = settings
        self.screen_size = settings.screen_rect.size
        self.screen_width, self.screen_height = self.screen_size

        # Dictionary of background image sources with counts
        self.image_sources = self.settings.bg_image_sources

        # List of layered background objects
        self.layers = []
        for image, count in self.image_sources.items():
            # Create a BackgroundObjectLayer for each image type
            objects = BackgroundObjectLayer(
                image, count, self.screen_size, paint=True, transparency=200
            )
            self.layers.append(objects)

    def build(self):
        """
        Assemble and return the complete background surface with stars, image layers, and nebulas.

        Returns:
            pygame.Surface: The rendered background surface.
        """
        base_surface = self._draw_first_layer()  # Starfield layer

        # Draw additional image layers
        for layer in self.layers:
            layer.draw(base_surface)

        # Draw randomly generated nebula clusters
        for cluster in self._create_nebulas_layer():
            for nebula in cluster:
                nebula.draw_nebulas(base_surface)

        return base_surface

    def _draw_first_layer(self):
        """
        Create the base background surface and populate it with faraway stars.

        Returns:
            pygame.Surface: The background with randomly placed stars.
        """
        surface = pygame.Surface(self.screen_size)
        surface = surface.convert()

        # Create a number of randomly placed stars
        for _ in range(self.settings.number_of_faraway_stars):
            color, rect = self.create_faraway_stars()
            surface.fill(color, rect)

        return surface

    def create_faraway_stars(self):
        """
        Generate a random faraway star's size, color, and position.

        Returns:
            tuple: (RGB color, pygame.Rect) defining the star's appearance and location.
        """
        sizes = [(1, 1), (2, 2), (3, 3)]
        colors = [
            (90, 120, 170), (90, 170, 200), 
            (190, 50, 20), (230, 170, 20), (150, 230, 240)
        ]
        width, height = choice(sizes)
        rect = pygame.Rect(
            randint(0, self.screen_width - width),
            randint(0, self.screen_height - height),
            width, height
        )
        return choice(colors), rect

    def _create_nebulas_layer(self):
        """
        Create multiple clusters of nebulas to enhance the depth of the background.

        Returns:
            list: A list of nebula clusters (each a list of BackgroundObjectLayer instances).
        """
        number_of_clusters = self.settings.number_of_faraway_stars // 15
        clusters = []
        for _ in range(number_of_clusters):
            cluster = self._create_nebula_cluster()
            clusters.append(cluster)
        return clusters

    def _create_nebula_cluster(self):
        """
        Create a single nebula cluster with multiple overlapping nebula images.

        Returns:
            list: A list of BackgroundObjectLayer instances representing the cluster.
        """
        nebulas_number = randint(5, 10)
        nebulas = self._find_nebula_images()

        # Choose a random nebula to determine cluster size
        rand_neb = pygame.image.load(choice(nebulas))
        rand_neb_rect = rand_neb.get_rect()
        width = rand_neb_rect.width * randint(2, 4)
        height = rand_neb_rect.height * randint(2, 4)

        # Define the area in which this cluster will be drawn
        rect = pygame.Rect(
            randint(0, self.screen_width - width),
            randint(0, self.screen_height - height),
            width, height
        )

        cluster = []
        cluster_size = rect.size

        # Populate the cluster with randomly selected nebula images
        for _ in range(nebulas_number):
            rand_nebula = choice(nebulas)
            count = 1
            obj = BackgroundObjectLayer(rand_nebula, count, cluster_size, offset=(rect.x, rect.y))
            cluster.append(obj)

        return cluster

    def _find_nebula_images(self):
        """
        Generate a list of file paths to nebula images.

        Returns:
            list: File paths to nebula image assets.
        """
        nebulas = []
        for number in range(1, 16):
            image_path = "images/nebulas/n_%d.png" % number
            nebulas.append(image_path)
        return nebulas