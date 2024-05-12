import sys
from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QMainWindow

from classes.pipetka import PipetkaWindow
from classes.spichka import SpichkaWindow


class SurfaceTension(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainUi.ui", self)
        self.setWindowTitle("Выбор модели")

        self.stbar_msecs = 3000  # Задержка сообщений в статусбаре
        self.g_var = 10  # Переменная ускорения свободного падения
        self.pi_var = 3.1415  # Число Пи

        self.initUI()

    def initUI(self):
        self.pipetka.clicked.connect(self.pipetkaOpenWindow)
        self.spichka.clicked.connect(self.spichkaOpenWindow)

    def pipetkaOpenWindow(self):
        pipetka = PipetkaWindow(self)
        pipetka.show()

    def spichkaOpenWindow(self):
        spichka = SpichkaWindow(self)
        spichka.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SurfaceTension()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
