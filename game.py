import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QDesktopWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class GameScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set up the main vertical layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set fonts
        font_large = QFont("Times New Roman", 40)  # Large font for question
        font_medium = QFont("Times New Roman", 20)  # Medium font for buttons

        # --- Question Label (Centered, 25% from top) ---
        self.question_label = QLabel("Placeholder Question?", self)
        self.question_label.setFont(font_large)
        self.question_label.setAlignment(Qt.AlignCenter)

        # Stretch to push the label 25% down
        layout.addStretch(1)
        layout.addWidget(self.question_label)
        layout.addStretch(1)  # Add space after question before buttons

        # --- Answer Buttons (Stacked Vertically) ---
        self.answer_buttons = {
            "Yes": QPushButton("Yes"),
            "No": QPushButton("No"),
            "Probably": QPushButton("Probably"),
            "Probably Not": QPushButton("Probably Not"),
            "I Don't Know": QPushButton("I Don't Know"),
        }

        # Apply font to buttons and stack them vertically
        for btn_text, btn in self.answer_buttons.items():
            btn.setFont(font_medium)
            layout.addWidget(btn)

        layout.addStretch(2)  # Extra stretch below buttons to keep spacing nice

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Guess Master - Game")
        self.setGeometry(100, 100, 800, 500)

        # Center the window on the screen
        self.center_window()

        # Set the main game screen as the central widget
        self.game_screen = GameScreen()
        self.setCentralWidget(self.game_screen)

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
