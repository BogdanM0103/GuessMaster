import sys

from PyQt5.QtWidgets import (
    QMainWindow, QStackedWidget, QDesktopWidget, QApplication
)

from res.StartScreen import StartScreen
from res.QuestionScreen import QuestionScreen
from res.GameOverScreen import GameOverScreen
from res.config import (
    APP_NAME
)

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 800, 500)
        self.center_window()

        # Create the QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create screens and add them to the stacked widget
        self.main_menu = StartScreen(self.stacked_widget)
        self.game_screen = QuestionScreen(self.stacked_widget)
        self.game_over_screen = GameOverScreen(self.stacked_widget)

        self.stacked_widget.addWidget(self.main_menu)  # Index 0
        self.stacked_widget.addWidget(self.game_screen)  # Index 1
        self.stacked_widget.addWidget(self.game_over_screen)  # Index 2

    def center_window(self):
        """Centers the main window on the user's screen."""
        frame_geom = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(screen_center)
        self.move(frame_geom.topLeft())
