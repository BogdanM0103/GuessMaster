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
        self.yes_button = QPushButton(YES, self)
        self.yes_button.setFont(self.title_label.font())
        self.yes_button.clicked.connect(self.handle_yes)

        self.no_button = QPushButton(NO, self)
        self.no_button.setFont(self.title_label.font())
        self.no_button.clicked.connect(self.handle_no)

        self.layout().addWidget(self.yes_button)
        self.layout().addWidget(self.no_button)

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
        self.show_yes_no_buttons()  # Show Yes/No initially

    def handle_yes(self):
        """Handles when the user confirms the guess was correct."""
        self.title_label.setText(SUCCESS.format(animal=self.predicted_animal))
        self.show_final_buttons()

    def handle_no(self):
        """Handles when the user says the guess was incorrect."""
        self.title_label.setText(FAILURE)
        self.show_final_buttons()

    def show_yes_no_buttons(self):
        """Shows Yes and No buttons at the start."""
        self.yes_button.setVisible(True)
        self.no_button.setVisible(True)
        self.play_again_button.setVisible(False)
        self.exit_button.setVisible(False)

    def show_final_buttons(self):
        """Replaces 'Yes' and 'No' with 'Play Again' and 'Exit'."""
        self.yes_button.setVisible(False)
        self.no_button.setVisible(False)
        self.play_again_button.setVisible(True)
        self.exit_button.setVisible(True)

    def play_again(self):
        """Restart game."""
        self.stacked_widget.setCurrentIndex(0)

    def exit_game(self):
        """Exit the application."""
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
