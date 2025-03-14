from res.BaseScreen import BaseScreen
from res.config import APP_NAME, START

class StartScreen(BaseScreen):
    def __init__(self, stacked_widget):
        super().__init__(
            stacked_widget, 
            title_text=APP_NAME, 
            button_text=START, 
            button_callback=self.start_game
        )

    def start_game(self):
        """Switch to the Game Screen"""
        self.stacked_widget.setCurrentIndex(1)
