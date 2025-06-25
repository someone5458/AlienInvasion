from settings import Settings

if __name__ == '__main__':
    # If this script is run directly, create the game settings instance and start the screen manager
    game = Settings()
    game.screen_manager.run()