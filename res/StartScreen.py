from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from res.config import (
    APP_NAME,
    FONT,
    FONT_SIZE_LARGE,
    FONT_SIZE_SMALL,
    START
)

class StartScreen(QWidget):
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

        # Title Label
        self.title_label = QLabel(APP_NAME, self)
        self.title_label.setFont(font_large)
        self.title_label.setAlignment(Qt.AlignCenter)

        # Start Button
        self.start_button = QPushButton(START, self)
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