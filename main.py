import sys
from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QMainWindow

from classes.kapillar import KapillarWindow
from classes.kolco import KolcoWindow
from classes.pipetka import PipetkaWindow
from classes.spichka import SpichkaWindow


class SurfaceTension(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainUi.ui", self)
        self.setWindowTitle("Выбор модели")

        self.stbar_msecs = 4000  # Задержка сообщений в статусбаре
        self.g_var = 9.81  # Переменная ускорения свободного падения
        self.pi_var = 3.1415  # Число Пи

        self.initUI()

    def initUI(self):
        self.pipetka.clicked.connect(self.pipetkaOpenWindow)
        self.spichka.clicked.connect(self.spichkaOpenWindow)
        self.kolco.clicked.connect(self.kolcoOpenWindow)
        self.kapillar.clicked.connect(self.kapillarOpenWindow)
        self.settings.clicked.connect(self.settingsOpenWindow)

    def pipetkaOpenWindow(self):
        pipetka = PipetkaWindow(self)
        pipetka.show()

    def spichkaOpenWindow(self):
        spichka = SpichkaWindow(self)
        spichka.show()

    def kolcoOpenWindow(self):
        kolco = KolcoWindow(self)
        kolco.show()

    def kapillarOpenWindow(self):
        kapillar = KapillarWindow(self)
        kapillar.show()

    def settingsOpenWindow(self):
        settings = SettingsWindow(self)
        settings.show()


class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/settings.ui", self)
        self.setWindowTitle("Настройки")
        self.parent = parent  # атрибут с родительским классом

        self.initUi()

    def initUi(self):
        self.g_var.setText(str(self.parent.g_var))
        self.pi_var.setText(str(self.parent.pi_var))

        self.save_btn.clicked.connect(self.save)

    def save(self):
        try:
            self.parent.g_var = float(self.g_var.toPlainText())
            self.parent.pi_var = float(self.pi_var.toPlainText())
        except ValueError:
            self.statusBar().showMessage(
                'Используйте "." вместо ","!',
                self.parent.stbar_msecs,
            )
            return
        self.parent.statusBar().showMessage(
            f"g = {self.parent.g_var}; pi = {self.parent.pi_var}",
            self.parent.stbar_msecs,
        )
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SurfaceTension()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
