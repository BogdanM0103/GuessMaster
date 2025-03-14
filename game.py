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
        self.stacked_widget = stacked_widget  # Reference to switch screens
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set fonts
        font_large = QFont("Times New Roman", 40)
        font_medium = QFont("Times New Roman", 20)

        # Title Label
        self.title_label = QLabel("Guess Master", self)
        self.title_label.setFont(font_large)
        self.title_label.setAlignment(Qt.AlignCenter)

        # Start Button
        self.start_button = QPushButton("Start", self)
        self.start_button.setFont(font_medium)
        self.start_button.setStyleSheet(self.button_styles())  # Apply hover effect
        self.start_button.clicked.connect(self.start_game)

        layout.addStretch(1)
        layout.addWidget(self.title_label)
        layout.addStretch(1)
        layout.addWidget(self.start_button)
        layout.addStretch(2)

    def start_game(self):
        """Switch to the Game Screen"""
        self.stacked_widget.setCurrentIndex(1)

    def button_styles(self):
        """Returns the stylesheet string for buttons with a hover effect."""
        return """
            QPushButton {
                background-color: lightgray;
                color: black;
                border: 2px solid black;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: yellow;
            }
        """

class GameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Reference to switch screens
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set fonts
        font_large = QFont("Times New Roman", 40)  
        font_medium = QFont("Times New Roman", 20)  

        # Question Label
        self.question_label = QLabel("Placeholder Question?", self)
        self.question_label.setFont(font_large)
        self.question_label.setAlignment(Qt.AlignCenter)

        layout.addStretch(1)
        layout.addWidget(self.question_label)
        layout.addStretch(1)

        # Answer Buttons (Stacked Vertically)
        self.answer_buttons = {
            "Yes": QPushButton("Yes"),
            "No": QPushButton("No"),
            "Probably": QPushButton("Probably"),
            "Probably Not": QPushButton("Probably Not"),
            "I Don't Know": QPushButton("I Don't Know"),
        }

        for btn_text, btn in self.answer_buttons.items():
            btn.setFont(font_medium)
            btn.setStyleSheet(self.button_styles())  
            btn.clicked.connect(lambda _, answer=btn_text: self.end_game("Lion"))  # Example animal
            layout.addWidget(btn)

        layout.addStretch(2)

    def end_game(self, predicted_animal):
        """Switch to the Game Over screen with a prediction"""
        self.stacked_widget.widget(2).set_prediction(predicted_animal)
        self.stacked_widget.setCurrentIndex(2)

    def button_styles(self):
        """Returns the stylesheet string for buttons with a hover effect."""
        return """
            QPushButton {
                background-color: lightgray;
                color: black;
                border: 2px solid black;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: yellow;
            }
        """

class GameOverScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set fonts
        font_large = QFont("Times New Roman", 40)
        font_medium = QFont("Times New Roman", 20)

        # Result Label (Will be updated dynamically)
        self.result_label = QLabel("You thought about a...", self)
        self.result_label.setFont(font_large)
        self.result_label.setAlignment(Qt.AlignCenter)

        # Exit Button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFont(font_medium)
        self.exit_button.setStyleSheet(self.button_styles())
        self.exit_button.clicked.connect(self.exit_game)

        layout.addStretch(1)
        layout.addWidget(self.result_label)
        layout.addStretch(1)
        layout.addWidget(self.exit_button)
        layout.addStretch(2)

    def set_prediction(self, animal):
        """Update the label to show the predicted animal"""
        self.result_label.setText(f"You thought about a {animal}!")

    def exit_game(self):
        """Exit the application"""
        QApplication.quit()

    def button_styles(self):
        """Returns the stylesheet string for buttons with a hover effect."""
        return """
            QPushButton {
                background-color: lightgray;
                color: black;
                border: 2px solid black;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: yellow;
            }
        """

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

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
