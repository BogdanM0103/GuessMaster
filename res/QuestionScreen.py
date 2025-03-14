from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QStackedWidget, QDesktopWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from res.config import (
    FONT,
    FONT_SIZE_LARGE,
    FONT_SIZE_SMALL,
    PLACEHOLDER_QUESTION,
    YES,
    NO,
    PROBABLY,
    PROBABLY_NOT,
    I_DONT_KNOW
)

class QuestionScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget  # Reference to switch screens
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set fonts
        font_large = QFont(FONT, FONT_SIZE_LARGE)  
        font_medium = QFont(FONT, FONT_SIZE_SMALL)  

        # Question Label
        self.question_label = QLabel(PLACEHOLDER_QUESTION, self)
        self.question_label.setFont(font_large)
        self.question_label.setAlignment(Qt.AlignCenter)

        layout.addStretch(1)
        layout.addWidget(self.question_label)
        layout.addStretch(1)

        # Answer Buttons (Stacked Vertically)
        self.answer_buttons = {
            YES: QPushButton(YES),
            NO: QPushButton(NO),
            PROBABLY: QPushButton(PROBABLY),
            PROBABLY_NOT: QPushButton(PROBABLY_NOT),
            I_DONT_KNOW: QPushButton(I_DONT_KNOW),
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