from PyQt5 import uic

from PyQt5.QtWidgets import QMainWindow


class PipetkaWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/pipetka.ui', self)
        self.parent = parent  # атрибут с родительским классом
