import sys

import sympy
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from sympy.parsing.sympy_parser import parse_expr


class KapillarWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/kapillar.ui", self)
        self.setWindowTitle("Модель капилляра")
        self.parent = parent  # атрибут с родительским классом

        self.objects = {
            "σ": self.sigma_var,
            "ρ": self.ro_var,
            "h": self.h_var,
            "m": self.m_var,
            "Fпн": self.Fpn_var,
            "Fтяж": self.Ft_var,
            "A": self.A_var,
            "Eп": self.Ep_var,
            "l": self.l_var,
            "R": self.R_var,
            "d": self.d_var,
        }  # Объекты текстовых полей по символам
        self.check_value = {
            "σ": [["Fпн", "l"], "Fpn/l"],
            "ρ": [["σ", "R", "h"], "(2*sigma)/(R*g*h)"],
            "h": [["σ", "ρ", "R"], "(2*sigma)/(R*ro*g)"],
            "m": [["R", "σ"], "(2*Pi*R*sigma)/g"],
            "Fпн": [["σ", "l"], "sigma*l"],
            "Fтяж": [["m"], "m*g"],
            "A": [["σ", "ρ"], "(4*Pi*sigma**2)/(ro*g)"],
            "Eп": [["σ", "ρ"], "(2*Pi*sigma**2)/(ro*g)"],
            "l": [["d"], "Pi*d"],
            "R": [["d"], "d/2"],
            "d": [["σ", "ρ", "h"], "(4*sigma)/(ro*g*h)"],
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
        sigma, ro, h, m, Fpn, Ft, A, Ep, l, R, d, Pi, g = sympy.symbols(
            "sigma ro h m Fpn Ft A Ep l R d Pi g"
        )
        # val - результат вычислений по формуле
        val = float(
            expr.evalf(
                subs={
                    sigma: self.sigma_var.toPlainText(),
                    ro: self.ro_var.toPlainText(),
                    h: self.h_var.toPlainText(),
                    m: self.m_var.toPlainText(),
                    Fpn: self.Fpn_var.toPlainText(),
                    Ft: self.Ft_var.toPlainText(),
                    A: self.A_var.toPlainText(),
                    Ep: self.Ep_var.toPlainText(),
                    l: self.l_var.toPlainText(),
                    R: self.R_var.toPlainText(),
                    d: self.d_var.toPlainText(),
                    Pi: self.parent.pi_var,
                    g: self.parent.g_var,
                }
            )
        )
        # Вычисленный результат округляется и выводится пользователю
        self.answer.setText(str(round(val, self.round.value())))
        self.statusBar().showMessage(
            "Ответ успешно вычислен!", self.parent.stbar_msecs
        )


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    from __abstract import SurfaceTension

    app = QApplication(sys.argv)
    parent = SurfaceTension()
    form = KapillarWindow(parent)
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
