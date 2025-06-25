from save_file import SaveFile

class GameStats:
    """
    Tracks and manages game statistics such as score, level, ships remaining,
    and persistent stats like high score or total games played.
    """

    def __init__(self, game):
        """
        Initializes game statistics and loads previously saved data.

        Args:
            game: Reference to the main game instance, used to access settings and save files.
        """
        self.game = game
        self.settings = game.settings
        self.save_file = SaveFile()

        # Core game state flags
        self.game_active = False  # True when the game is currently running

        # Persistent statistics
        self.high_score = 0
        self.aliens_destroyed = 0
        self.ships_lost = 0
        self.games_played = 0

        # Load previous session statistics
        self._load_statistics()

        # Initialize in-game (dynamic) stats
        self.reset_stats()

    def reset_stats(self):
        """
        Resets statistics that are re-initialized at the start of each game.
        """
        self.ships_left = self.settings.ship_limit  # Remaining player lives
        self.score = 0  # Player's score starts from zero
        self.level = 1  # Starting level
        self.settings.initialize_dynamic_settings()  # Reset any gameplay-modifying settings

    def _load_statistics(self):
        """
        Loads persistent game statistics from an external save file.
        Uses the SaveFile class to retrieve and assign values.
        """
        self.save_file._load_data()  # Ensure file is read and up to date
        saved_data = self.save_file._load_data()  # Load saved dictionary of stats
        for category, value in saved_data.items():
            setattr(self, category, value)  # Dynamically set each stat as an attribute