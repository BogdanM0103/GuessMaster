from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
from res.BaseScreen import BaseScreen
from res.config import PLACEHOLDER_QUESTION, YES, NO, PROBABLY, PROBABLY_NOT, I_DONT_KNOW

class QuestionScreen(BaseScreen):
    def __init__(self, stacked_widget):
        super().__init__(stacked_widget, title_text=PLACEHOLDER_QUESTION)
        self.init_buttons()

    def init_buttons(self):
        """Creates answer buttons dynamically."""
        font_medium = QFont("Times New Roman", 20)
        answers = [YES, NO, PROBABLY, PROBABLY_NOT, I_DONT_KNOW]

        for answer in answers:
            btn = QPushButton(answer, self)
            btn.setFont(font_medium)
            btn.clicked.connect(lambda _, ans=answer: self.end_game("Lion"))  # Example
            self.layout().addWidget(btn)

    def end_game(self, predicted_animal):
        """Switch to the Game Over screen with a prediction"""
        self.stacked_widget.widget(2).set_prediction(predicted_animal)
        self.stacked_widget.setCurrentIndex(2)
