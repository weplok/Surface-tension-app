from PyQt5.QtWidgets import QMainWindow


class SurfaceTension(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stbar_msecs = 3000  # Задержка сообщений в статусбаре
        self.g_var = 9.81  # Переменная ускорения свободного падения
        self.pi_var = 3.1415  # Число Пи
