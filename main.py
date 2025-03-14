import sys

from PyQt5.QtWidgets import (
    QApplication
)

from PyQt5.QtGui import QFont
from res.App import App

from res.config import (
    FONT,
    FONT_SIZE_LARGE
)

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont(FONT, FONT_SIZE_LARGE))  # Global font for the app

    window = App()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()