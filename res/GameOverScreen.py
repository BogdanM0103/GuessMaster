from PyQt5.QtWidgets import QPushButton
from res.BaseScreen import BaseScreen
from res.config import GOOD_GUESS, YES, NO, EXIT, REPLAY, SUCCESS, FAILURE, GUESS_ANSWER

class GameOverScreen(BaseScreen):
    def __init__(self, stacked_widget):
        super().__init__(stacked_widget, title_text=GOOD_GUESS)
        self.predicted_animal = ""
        self.init_buttons()

    def init_buttons(self):
        """Creates Yes/No buttons dynamically."""
        buttons = {
            YES: self.handle_yes,
            NO: self.handle_no,
        }

        for text, callback in buttons.items():
            btn = QPushButton(text, self)
            btn.setFont(self.title_label.font())  # Same font size
            btn.clicked.connect(callback)
            self.layout().addWidget(btn)

        self.play_again_button = QPushButton(REPLAY, self)
        self.play_again_button.setVisible(False)
        self.play_again_button.setFont(self.title_label.font())
        self.play_again_button.clicked.connect(self.play_again)
        self.layout().addWidget(self.play_again_button)

        self.exit_button = QPushButton(EXIT, self)
        self.exit_button.setVisible(False)
        self.exit_button.setFont(self.title_label.font())
        self.exit_button.clicked.connect(self.exit_game)
        self.layout().addWidget(self.exit_button)

    def set_prediction(self, animal):
        """Update the label to show the guessed animal."""
        self.predicted_animal = animal
        self.title_label.setText(GUESS_ANSWER.format(animal=animal))

    def handle_yes(self):
        """Handles when the user confirms the guess was correct."""
        self.title_label.setText(SUCCESS.format(animal=self.predicted_animal))
        self.show_final_buttons()

    def handle_no(self):
        """Handles when the user says the guess was incorrect."""
        self.title_label.setText(FAILURE)
        self.show_final_buttons()

    def show_final_buttons(self):
        """Replaces 'Yes' and 'No' with 'Play Again' and 'Exit'."""
        self.play_again_button.setVisible(True)
        self.exit_button.setVisible(True)

    def play_again(self):
        """Restart game."""
        self.stacked_widget.setCurrentIndex(0)

    def exit_game(self):
        """Exit the application."""
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
