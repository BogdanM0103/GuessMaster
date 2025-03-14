import sys

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QStackedWidget, QDesktopWidget, QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from StartScreen import StartScreen
from QuestionScreen import QuestionScreen
from GameOverScreen import GameOverScreen

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Guess Master")
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
        
def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Times New Roman", 40))  # Global font for the app

    window = App()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
