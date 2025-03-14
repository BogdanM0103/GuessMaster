import sys

from PyQt5.QtWidgets import (
    QApplication
)

from PyQt5.QtGui import QFont
from res.App import App

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Times New Roman", 40))  # Global font for the app

    window = App()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()