import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from res.config import FONT, FONT_SIZE_LARGE, FONT_SIZE_SMALL

class BaseScreen(QWidget):
    def __init__(self, stacked_widget, title_text="Title", button_text=None, button_callback=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui(title_text, button_text, button_callback)
        self.load_stylesheet()  # Load external styles

    def init_ui(self, title_text, button_text, button_callback):
        """Initialize the UI with a title and an optional button."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set fonts
        font_large = QFont(FONT, FONT_SIZE_LARGE)
        font_medium = QFont(FONT, FONT_SIZE_SMALL)

        # Title Label
        self.title_label = QLabel(title_text, self)
        self.title_label.setFont(font_large)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.title_label)
        layout.addStretch(1)

        # Button (if provided)
        if button_text and button_callback:
            self.button = QPushButton(button_text, self)
            self.button.setFont(font_medium)
            self.button.clicked.connect(button_callback)
            layout.addWidget(self.button)
            layout.addStretch(2)

    def load_stylesheet(self):
        """Loads an external stylesheet for the application."""
        stylesheet_path = os.path.join(os.path.dirname(__file__), "styles.qss")

        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Warning: {stylesheet_path} not found. Default styles will be used.")
