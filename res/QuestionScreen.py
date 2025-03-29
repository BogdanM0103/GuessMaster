from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QFont
from res.BaseScreen import BaseScreen
from res.config import YES, NO, PROBABLY, PROBABLY_NOT, I_DONT_KNOW, FONT, FONT_SIZE_SMALL, FONT_SIZE_LARGE
from game_session import GameSession

class QuestionScreen(BaseScreen):
    def __init__(self, stacked_widget):
        self.stacked_widget = stacked_widget
        self.game = GameSession()

        # Obținem prima întrebare
        self.current_question = self.game.get_current_question() or "Let's begin!"

        # Inițializăm ecranul de bază cu întrebarea
        super().__init__(stacked_widget, title_text=self.current_question)

        # Referință la titlu pentru a-l actualiza ulterior
        self.title_label.setFont(QFont(FONT, FONT_SIZE_LARGE))
        self.title_label.setWordWrap(True)

        # Inițializăm butoanele
        self.init_buttons()

    def init_buttons(self):
        font_medium = QFont(FONT, FONT_SIZE_SMALL)
        answers = [YES, NO, PROBABLY, PROBABLY_NOT, I_DONT_KNOW]

        for answer in answers:
            btn = QPushButton(answer, self)
            btn.setFont(font_medium)
            btn.clicked.connect(lambda _, ans=answer: self.handle_answer(ans))
            self.layout().addWidget(btn)

    def handle_answer(self, answer):
        self.game.submit_answer(answer)

        next_question = self.game.get_current_question()

        if next_question:
            self.update_question(next_question)
        else:
            predicted = self.game.get_prediction() or "Unknown"
            self.end_game(predicted)

    def update_question(self, new_text):
        self.title_label.setText(new_text)

    def end_game(self, predicted_animal):
        self.stacked_widget.widget(2).set_prediction(predicted_animal)
        self.stacked_widget.setCurrentIndex(2)
