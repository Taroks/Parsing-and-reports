import sys
from PySide6.QtWidgets import QApplication
from front import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())