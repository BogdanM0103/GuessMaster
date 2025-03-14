from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from res.config import (
    FONT,
    FONT_SIZE_LARGE,
    FONT_SIZE_SMALL,
    GOOD_GUESS,
    YES,
    NO,
    EXIT,
    REPLAY,
    SUCCESS,
    FAILURE,
    GUESS_ANSWER
)

class GameOverScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.predicted_animal = ""  # Store the predicted animal
        self.init_ui()

    def init_ui(self):
        """Initializes the Game Over screen layout."""
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        font_large = QFont(FONT, FONT_SIZE_LARGE)
        font_medium = QFont(FONT, FONT_SIZE_SMALL)

        # --- Predicted Animal Label ---
        self.result_label = QLabel(GUESS_ANSWER, self)
        self.result_label.setFont(font_large)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.layout.addStretch(1)
        self.layout.addWidget(self.result_label)
        self.layout.addStretch(1)

        # --- Question: Have I guessed correctly? ---
        self.confirmation_label = QLabel(GOOD_GUESS, self)
        self.confirmation_label.setFont(font_medium)
        self.confirmation_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.confirmation_label)

        # --- Yes / No Buttons ---
        self.button_layout = QVBoxLayout()

        self.yes_button = QPushButton(YES)
        self.yes_button.setFont(font_medium)
        self.yes_button.setStyleSheet(self.button_styles())
        self.yes_button.clicked.connect(self.handle_yes)

        self.no_button = QPushButton(NO)
        self.no_button.setFont(font_medium)
        self.no_button.setStyleSheet(self.button_styles())
        self.no_button.clicked.connect(self.handle_no)

        self.button_layout.addWidget(self.yes_button)
        self.button_layout.addWidget(self.no_button)

        self.layout.addLayout(self.button_layout)

        # --- Exit Button (Initially Hidden) ---
        self.exit_button = QPushButton(EXIT)
        self.exit_button.setFont(font_medium)
        self.exit_button.setStyleSheet(self.button_styles())
        self.exit_button.clicked.connect(self.exit_game)
        self.exit_button.setVisible(False)

        # --- Play Again Button (Initially Hidden) ---
        self.play_again_button = QPushButton(REPLAY)
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
        self.predicted_animal = animal  # Store for later use
        self.result_label.setText(GUESS_ANSWER.format(animal=animal))  # Format correctly
        self.reset_buttons()

    def handle_yes(self):
        """Handles when the user confirms the guess was correct."""
        self.result_label.setText(SUCCESS.format(animal=self.predicted_animal))
        self.switch_to_play_again()

    def handle_no(self):
        """Handles when the user says the guess was incorrect."""
        self.result_label.setText(FAILURE)
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
