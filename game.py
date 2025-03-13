import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QStackedWidget, QDesktopWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainMenuScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Reference to stacked widget to switch screens
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set fonts
        font_large = QFont("Times New Roman", 40)
        font_medium = QFont("Times New Roman", 20)

        # --- Title Label ---
        self.title_label = QLabel("Guess Master", self)
        self.title_label.setFont(font_large)
        self.title_label.setAlignment(Qt.AlignCenter)

        # --- Start Button ---
        self.start_button = QPushButton("Start", self)
        self.start_button.setFont(font_medium)
        self.start_button.clicked.connect(self.start_game)

        layout.addStretch(1)
        layout.addWidget(self.title_label)
        layout.addStretch(1)
        layout.addWidget(self.start_button)
        layout.addStretch(2)

    def start_game(self):
        """Switch to the Game Screen"""
        self.stacked_widget.setCurrentIndex(1)  # Switch to GameScreen

class GameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Reference to stacked widget to switch screens
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set fonts
        font_large = QFont("Times New Roman", 40)  # Large font for question
        font_medium = QFont("Times New Roman", 20)  # Medium font for buttons

        # --- Question Label (Centered, 25% from top) ---
        self.question_label = QLabel("Placeholder Question?", self)
        self.question_label.setFont(font_large)
        self.question_label.setAlignment(Qt.AlignCenter)

        layout.addStretch(1)
        layout.addWidget(self.question_label)
        layout.addStretch(1)

        # --- Answer Buttons (Stacked Vertically) ---
        self.answer_buttons = {
            "Yes": QPushButton("Yes"),
            "No": QPushButton("No"),
            "Probably": QPushButton("Probably"),
            "Probably Not": QPushButton("Probably Not"),
            "I Don't Know": QPushButton("I Don't Know"),
        }

        for btn_text, btn in self.answer_buttons.items():
            btn.setFont(font_medium)
            layout.addWidget(btn)

        layout.addStretch(2)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Guess Master")
        self.setGeometry(100, 100, 800, 500)
        self.center_window()

        # Create the QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create screens and add them to the stacked widget
        self.main_menu = MainMenuScreen(self.stacked_widget)
        self.game_screen = GameScreen(self.stacked_widget)

        self.stacked_widget.addWidget(self.main_menu)  # Index 0
        self.stacked_widget.addWidget(self.game_screen)  # Index 1

    def center_window(self):
        """Centers the main window on the user's screen."""
        frame_geom = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(screen_center)
        self.move(frame_geom.topLeft())

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Times New Roman", 40))  # Global font for the app

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
