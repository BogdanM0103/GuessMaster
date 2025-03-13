import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QDesktopWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Guess Master - Main Menu")
        self.setGeometry(100, 100, 600, 400)  # initial (x, y, width, height)

        # Center the window on the screen
        self.center_window()

        # Create a central widget (no layout, we'll do manual placement)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the label and button as children of central_widget
        self.welcome_label = QLabel("Guess Master", central_widget)

        self.start_button = QPushButton("Start", central_widget)
        # Override the default app font for this button only
        button_font = QFont("Times New Roman", 20)
        self.start_button.setFont(button_font)

        # Position the widgets
        self.position_widgets()

    def center_window(self):
        """
        Centers the main window on the user's screen.
        """
        frame_geom = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geom.moveCenter(screen_center)
        self.move(frame_geom.topLeft())

    def resizeEvent(self, event):
        """
        Called whenever the window is resized (including on show).
        We recalculate widget positions to maintain the same proportions.
        """
        super().resizeEvent(event)
        self.position_widgets()

    def position_widgets(self):
        """
        Positions the label and button using absolute coordinates so that:
         - Label is at 25% of the window's height.
         - Button is at 50% of the window's height.
         - Both are horizontally centered.
        """
        w = self.centralWidget().width()
        h = self.centralWidget().height()

        # --- Position the welcome label at 25% of height, horizontally centered ---
        label_width = self.welcome_label.sizeHint().width()
        label_height = self.welcome_label.sizeHint().height()
        label_x = (w - label_width) // 2
        label_y = int(h * 0.25) - (label_height // 2)
        self.welcome_label.move(label_x, label_y)

        # --- Position the start button at 50% of height, horizontally centered ---
        button_width = self.start_button.sizeHint().width()
        button_height = self.start_button.sizeHint().height()
        button_x = (w - button_width) // 2
        button_y = int(h * 0.50) - (button_height // 2)
        self.start_button.move(button_x, button_y)

def main():
    app = QApplication(sys.argv)
    # Set the default font for the entire application to Times New Roman, size 40
    app.setFont(QFont("Times New Roman", 40))

    window = MainMenu()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
