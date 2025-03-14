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
        """Initializes the Game Over screen layout."""
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        font_large = QFont("Times New Roman", 40)
        font_medium = QFont("Times New Roman", 20)

        # --- Predicted Animal Label ---
        self.result_label = QLabel("You thought about...", self)
        self.result_label.setFont(font_large)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.layout.addStretch(1)
        self.layout.addWidget(self.result_label)
        self.layout.addStretch(1)

        # --- Question: Have I guessed correctly? ---
        self.confirmation_label = QLabel("Have I guessed correct?", self)
        self.confirmation_label.setFont(font_medium)
        self.confirmation_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.confirmation_label)

        # --- Yes / No Buttons ---
        self.button_layout = QVBoxLayout()

        self.yes_button = QPushButton("Yes")
        self.yes_button.setFont(font_medium)
        self.yes_button.setStyleSheet(self.button_styles())
        self.yes_button.clicked.connect(self.handle_yes)

        self.no_button = QPushButton("No")
        self.no_button.setFont(font_medium)
        self.no_button.setStyleSheet(self.button_styles())
        self.no_button.clicked.connect(self.handle_no)

        self.button_layout.addWidget(self.yes_button)
        self.button_layout.addWidget(self.no_button)

        self.layout.addLayout(self.button_layout)

        # --- Exit Button (Initially Hidden) ---
        self.exit_button = QPushButton("Exit")
        self.exit_button.setFont(font_medium)
        self.exit_button.setStyleSheet(self.button_styles())
        self.exit_button.clicked.connect(self.exit_game)
        self.exit_button.setVisible(False)

        # --- Play Again Button (Initially Hidden) ---
        self.play_again_button = QPushButton("Play Again")
        self.play_again_button.setFont(font_medium)
        self.play_again_button.setStyleSheet(self.button_styles())
        self.play_again_button.clicked.connect(self.play_again)
        self.play_again_button.setVisible(False)

        self.layout.addStretch(1)
        self.layout.addWidget(self.play_again_button)
        self.layout.addWidget(self.exit_button)
        self.layout.addStretch(2)

    def set_prediction(self, animal):
        """Update the label to show the guessed animal."""
        self.result_label.setText(f"You thought about a {animal}!")
        self.reset_buttons()

    def handle_yes(self):
        """Handles when the user confirms the guess was correct."""
        self.result_label.setText("Yay! I guessed correctly! 🎉")
        self.switch_to_play_again()

    def handle_no(self):
        """Handles when the user says the guess was incorrect."""
        self.result_label.setText("Oh no! I'll try to improve next time. 🤔")
        self.switch_to_play_again()

    def switch_to_play_again(self):
        """Replaces 'Yes' and 'No' with 'Play Again' and 'Exit'."""
        self.yes_button.setVisible(False)
        self.no_button.setVisible(False)
        self.confirmation_label.setVisible(False)
        
        self.play_again_button.setVisible(True)
        self.exit_button.setVisible(True)

    def reset_buttons(self):
        """Resets the buttons for when the screen is revisited."""
        self.yes_button.setVisible(True)
        self.no_button.setVisible(True)
        self.confirmation_label.setVisible(True)

        self.play_again_button.setVisible(False)
        self.exit_button.setVisible(False)

    def play_again(self):
        """Restarts the game and goes back to the main menu."""
        self.stacked_widget.setCurrentIndex(0)  # Switch back to Main Menu

    def exit_game(self):
        """Exit the application."""
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()

    def button_styles(self):
        """Returns a stylesheet string for styling buttons."""
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
