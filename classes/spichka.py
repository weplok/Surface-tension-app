import sys

import sympy
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from sympy.parsing.sympy_parser import parse_expr


class SpichkaWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/spichka.ui", self)
        self.setWindowTitle("Модель спички")
        self.parent = parent  # атрибут с родительским классом

        self.objects = {
            "σ": self.sigma_var,
            "m": self.m_var,
            "Fпн": self.Fpn_var,
            "Fтяж": self.Ft_var,
            "l": self.l_var,
        }  # Объекты текстовых полей по символам
        self.check_value = {
            "σ": [["Fпн", "l"], "Fpn/l"],
            "m": [["Fтяж"], "Ft/g"],
            "Fпн": [["σ", "l"], "sigma*l"],
            "Fтяж": [["m"], "m*g"],
            "l": [["Fпн", "σ"], "Fpn/sigma"],
        }  # Необходимые для вычисления значения и формула

        self.initUi()

    def initUi(self):
        self.calculate_btn.clicked.connect(self.calculate)

    def calculate(self):
        calc_value = self.find.currentText()  # Вычисляемое значение

        for value in self.check_value[calc_value][0]:
            object_text = self.objects[value].toPlainText()
            # Проверяется, указаны ли необходимые значения для вычисления
            if object_text == "":
                self.statusBar().showMessage(
                    f"Сначала вычислите: {value}!", self.parent.stbar_msecs
                )
                return
            # Проверяется, что указанные значения - числа
            try:
                float(object_text)
            except ValueError:
                self.statusBar().showMessage(
                    "Значения - только числа!", self.parent.stbar_msecs
                )
                return

        # expr - объект формулы
        expr = parse_expr(self.check_value[calc_value][1])
        # Далее создаются объекты символов в формуле
        sigma, m, Fpn, Ft, l, Pi, g = sympy.symbols("sigma m Fpn Ft l Pi g")
        # val - результат вычислений по формуле
        val = float(
            expr.evalf(
                subs={
                    sigma: self.sigma_var.toPlainText(),
                    m: self.m_var.toPlainText(),
                    Fpn: self.Fpn_var.toPlainText(),
                    Ft: self.Ft_var.toPlainText(),
                    l: self.l_var.toPlainText(),
                    Pi: self.parent.pi_var,
                    g: self.parent.g_var,
                }
            )
        )
        # Вычисленный результат округляется и выводится пользователю
        self.answer.setText(str(round(val, self.round.value())))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SpichkaWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
