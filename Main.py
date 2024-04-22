import sys

from PyQt5.QtWidgets import QApplication

from entity.MainWindow import MainWindow

# if __name__ == '__main__':
# app = QApplication(sys.argv)
# window = MyWindow()
# window.show()
# sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
