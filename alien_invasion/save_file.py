import json

class SaveFile:
    """
    A class for managing game statistics saving and loading using a JSON file.
    """

    def __init__(self):
        """
        Initializes the SaveFile object with default statistics and file name.
        """
        self.file_name = "saved_statistics.json"
        self.save_data = {
            "high_score": 0,
            "aliens_destroyed": 0,
            "ships_lost": 0,
            "games_played": 0
        }

    def _update_data(self, stats):
        """
        Updates internal save_data dictionary with new values from the current game stats 
        if they are higher than the existing values.

        Args:
            stats: An object containing the current game statistics.
        """
        self.active_data = {
            "high_score": stats.high_score,
            "aliens_destroyed": stats.aliens_destroyed,
            "ships_lost": stats.ships_lost,
            "games_played": stats.games_played
        }

        # Update only if the new value is higher
        for category, value in self.save_data.items():
            active_value = self.active_data.get(category)
            if active_value > value:
                self.save_data[category] = active_value

    def _load_data(self):
        """
        Loads saved statistics from a JSON file. If the file does not exist or fails to load,
        it initializes the file with default data.

        Returns:
            dict: The loaded (or default) save data.
        """
        try:
            with open(self.file_name, "r") as file:
                saved_data = json.load(file)
                self.save_data.update(saved_data)
                return self.save_data
        except:
            self._save_data()
            return self.save_data

    def _save_data(self):
        """
        Saves the current save_data dictionary to the JSON file.
        """
        with open(self.file_name, "w") as file:
            json.dump(self.save_data, file)

    def save(self, stats):
        """
        Public method to update and save the statistics.

        Args:
            stats: An object containing the current game statistics.
        """
        self._update_data(stats)
        self._save_data()

    def reset_data(self):
        """
        Resets all saved statistics to 0 and writes the reset to the file.
        """
        for category in self.save_data.keys():
            self.save_data[category] = 0
        self._save_data()